"use strict";

const $ = id => document.getElementById(id);
const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const money = amount => new Intl.NumberFormat("vi-VN", {style:"currency",currency:"VND"}).format(Number(amount));
const icons = ["🥛","☕","🍑","💧","🍞","🍜","🥔","🍪","🧻"];
const tints = ["#e9eff8","#f1e9e0","#fff0e2","#e5f1f5","#f6eddf","#f4e7df","#f7efd8","#eee8df","#e8eee8"];
let products = [], cart = {items:[]}, orders = [], category = "all", busy = false, loaded = false;
let customerId, orderIds;
try {
  customerId = localStorage.getItem("shop.customer");
  if (!/^[0-9a-f]{8}-[0-9a-f-]{27}$/i.test(customerId || "")) {
    customerId = crypto.randomUUID();
    localStorage.setItem("shop.customer", customerId);
  }
  orderIds = JSON.parse(localStorage.getItem("shop.orders") || "[]");
  if (!Array.isArray(orderIds)) orderIds = [];
  orderIds = orderIds.filter(id => typeof id === "string" && /^[0-9a-f-]{36}$/i.test(id)).slice(0,10);
} catch {
  customerId = crypto.randomUUID();
  orderIds = [];
}
const iconFor = id => icons[parseInt(id.slice(-4),16)-1] || "🛍️";
const productFor = id => products.find(p => p.id === id);

async function api(path, method="GET", body) {
  const response = await fetch(path, {method, headers:body ? {"Content-Type":"application/json"} : {}, body:body ? JSON.stringify(body) : undefined});
  if (!response.ok) {
    const result = await response.json().catch(() => ({}));
    const friendly = {"Cart is empty":"Giỏ hàng đang trống. Hãy thêm sản phẩm trước khi đặt đơn.","Product not found":"Không tìm thấy sản phẩm.","Product is unavailable":"Sản phẩm hiện ngừng bán.","Cart not found":"Không tìm thấy giỏ hàng.","A product in the cart is unavailable":"Một sản phẩm trong giỏ đã ngừng bán.","Order not found":"Không tìm thấy đơn hàng."};
    const detail = typeof result.detail === "string" ? result.detail : "Dữ liệu chưa hợp lệ. Vui lòng kiểm tra lại.";
    const error = new Error(friendly[detail] || detail);
    error.status = response.status;
    throw error;
  }
  return response.status === 204 ? null : response.json();
}
function message(text, error=false) {
  $("message").textContent = text;
  $("message").className = "message" + (error ? " error" : "");
  $("message").hidden = false;
}
function renderProducts() {
  if (!loaded) {
    $("products").innerHTML = '<p class="empty">Đang tải sản phẩm. Nếu kết nối bị gián đoạn, hãy chọn Làm mới.</p>';
    return;
  }
  const term = $("search").value.trim().toLocaleLowerCase("vi");
  const visible = products.filter(p => (category === "all" || parseInt(p.category_id.slice(-4),16) === Number(category)) && (p.name+" "+p.description).toLocaleLowerCase("vi").includes(term));
  $("product-count").textContent = `(${visible.length})`;
  $("products").innerHTML = visible.length ? visible.map(p => `<article class="product">
    <button class="product-visual" data-detail="${p.id}" style="--tint:${tints[parseInt(p.id.slice(-4),16)-1] || "#edf1ed"}" aria-label="Xem ${escapeHtml(p.name)}"><span aria-hidden="true">${iconFor(p.id)}</span></button>
    <div class="product-info"><button class="product-name" data-detail="${p.id}">${escapeHtml(p.name)}</button><p class="product-description">${escapeHtml(p.description)}</p>
    <div class="product-bottom"><span class="price">${money(p.price.amount)}</span><button class="add" data-add="${p.id}" aria-label="Thêm ${escapeHtml(p.name)} vào giỏ" ${busy ? "disabled" : ""}>+</button></div></div></article>`).join("") : '<p class="empty">Không tìm thấy món phù hợp. Thử tên khác nhé.</p>';
}
function renderCart() {
  const count = cart.items.reduce((sum,item) => sum + item.quantity,0);
  $("cart-count").textContent = count;
  $("cart-label").textContent = `${count} món`;
  $("cart-items").innerHTML = cart.items.length ? cart.items.map(item => {
    const p = productFor(item.product_id);
    return `<div class="cart-item"><span class="item-icon" aria-hidden="true">${iconFor(item.product_id)}</span><div><div class="item-name">${escapeHtml(p?.name || "Sản phẩm ngừng bán")}</div>
    <div class="item-bottom"><div class="quantity"><button data-quantity="${item.product_id}" data-value="${item.quantity-1}" aria-label="Giảm số lượng ${escapeHtml(p?.name || "sản phẩm")}" ${busy ? "disabled" : ""}>−</button><span>${item.quantity}</span><button data-quantity="${item.product_id}" data-value="${item.quantity+1}" aria-label="Tăng số lượng ${escapeHtml(p?.name || "sản phẩm")}" ${busy || item.quantity>=99 ? "disabled" : ""}>+</button></div><span class="item-price">${p ? money(Number(p.price.amount)*item.quantity) : "—"}</span></div>
    <button class="remove" data-remove="${item.product_id}" ${busy ? "disabled" : ""}>Xóa</button></div></div>`;
  }).join("") : '<p class="empty"><span class="empty-symbol" aria-hidden="true">🛒</span>Giỏ hàng còn trống.<br>Thêm một món bạn thích nhé.</p>';
  $("cart-total").textContent = money(cart.items.reduce((sum,item) => sum + Number(productFor(item.product_id)?.price.amount || 0)*item.quantity,0));
  $("checkout").disabled = busy || !count;
  $("create-order").disabled = busy || !count;
}
function renderOrders() {
  const labels = {pending:"Chờ thanh toán",paid:"Đã thanh toán",cancelled:"Đã hủy",completed:"Hoàn tất"};
  $("orders").innerHTML = orders.length ? orders.map(order => `<div class="order"><div class="order-top"><span>#${escapeHtml(order.id.slice(0,8).toUpperCase())}</span><span class="status ${escapeHtml(order.status)}">${labels[order.status] || escapeHtml(order.status)}</span></div><p class="order-list">${order.items.map(item => `${escapeHtml(item.product_name)} × ${item.quantity}`).join("<br>")}</p><div class="order-total"><strong>${money(order.total.amount)}</strong>${order.status === "pending" ? `<button class="cancel" data-cancel="${order.id}" ${busy ? "disabled" : ""}>Hủy đơn</button>` : ""}</div></div>`).join("") : '<p class="empty">Chưa có đơn hàng.<br>Món ngon đang đợi bạn chọn.</p>';
  $("refresh").disabled = busy;
}
function render() { renderProducts(); renderCart(); renderOrders(); }
async function refresh() {
  const [nextProducts,nextCart,nextOrders] = await Promise.all([
    api("/products"), api(`/cart?customer_id=${customerId}`),
    Promise.all(orderIds.map(id => api(`/orders/${id}`).catch(error => {
      if (error.status === 404) return null;
      throw error;
    })))
  ]);
  products = nextProducts; cart = nextCart; orders = nextOrders.filter(Boolean); loaded = true;
}
async function perform(action, success) {
  if (busy) return;
  busy = true; render();
  try { await action(); await refresh(); if (success) message(success); }
  catch (error) { message(error instanceof TypeError ? "Chưa kết nối được cửa hàng. Hãy thử Làm mới." : error.message, true); }
  finally { busy = false; render(); }
}
async function add(id) {
  await perform(() => api("/cart/items", "POST", {customer_id:customerId,product_id:id,quantity:1}), "Đã thêm sản phẩm vào giỏ hàng.");
}
async function order(path) {
  await perform(async () => {
    const result = await api(path, "POST", {customer_id:customerId});
    orderIds = [result.order_id,...orderIds].slice(0,10);
    try { localStorage.setItem("shop.orders", JSON.stringify(orderIds)); } catch { /* Session remains usable. */ }
  }, path.includes("checkout") ? "Thanh toán demo thành công. Bạn không bị trừ tiền thật." : "Đã tạo đơn chờ thanh toán. Bạn có thể thử hủy ở bên dưới.");
}
$("search").addEventListener("input", renderProducts);
$("filters").addEventListener("click", event => {
  const button = event.target.closest("[data-category]");
  if (!button) return;
  category = button.dataset.category;
  document.querySelectorAll("[data-category]").forEach(b => { b.classList.toggle("active", b === button); b.setAttribute("aria-pressed", b === button ? "true" : "false"); });
  renderProducts();
});
document.addEventListener("click", async event => {
  const button = event.target.closest("button");
  if (!button || button.disabled || busy) return;
  const data = button.dataset;
  if (data.add) { $("product-dialog").close(); await add(data.add); }
  if (data.quantity || data.remove) {
    const id = data.quantity || data.remove, quantity = Number(data.value || 0);
    await perform(() => quantity === 0 ? api(`/cart/items/${id}?customer_id=${customerId}`, "DELETE") : api(`/cart/items/${id}`, "PATCH", {customer_id:customerId,quantity}));
  }
  if (data.cancel) await perform(() => api(`/orders/${data.cancel}/cancel`, "POST"), "Đã hủy đơn hàng.");
  if (data.detail) {
    try {
      const p = await api(`/products/${data.detail}`);
      $("product-detail").innerHTML = `<div class="detail-icon" aria-hidden="true">${iconFor(p.id)}</div><h2 id="detail-title">${escapeHtml(p.name)}</h2><p class="detail-description">${escapeHtml(p.description)}</p><p class="detail-price">${money(p.price.amount)}</p><button class="button primary" data-add="${p.id}">Thêm vào giỏ hàng</button>`;
      if (!$("product-dialog").open) $("product-dialog").showModal();
    } catch (error) { message(error.message,true); }
  }
});
$("checkout").addEventListener("click", () => order("/orders/checkout"));
$("create-order").addEventListener("click", () => order("/orders"));
$("refresh").addEventListener("click", () => perform(async () => {}, "Đã cập nhật giỏ hàng và đơn hàng."));
$("close-dialog").addEventListener("click", () => $("product-dialog").close());
perform(async () => {});
