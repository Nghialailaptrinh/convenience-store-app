from uuid import UUID

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from infrastructure.data.configurations import Base, ProductRecord
from infrastructure.data.migrations.link_users_to_customers import link_users_to_customers


def initialise_demo(engine: Engine) -> None:
    """Explicit demo startup only. Seed missing products without resetting user data."""
    Base.metadata.create_all(engine)
    link_users_to_customers(engine)
    products = [
        (1, "Sữa tươi nguyên chất", "Hộp 1 lít · Không đường", "32000", 1),
        (2, "Cà phê sữa đá", "Lon 235 ml · Đậm vị cà phê Việt", "18000", 1),
        (3, "Trà đào", "Chai 455 ml · Thanh mát mỗi ngày", "14000", 1),
        (4, "Nước khoáng", "Chai 500 ml · Tinh khiết", "7000", 1),
        (5, "Bánh mì sandwich", "Gói 200 g · Mềm thơm", "25000", 2),
        (6, "Mì ly hải sản", "Ly 65 g · Tiện lợi trong 3 phút", "16000", 2),
        (7, "Snack khoai tây", "Gói 60 g · Vị muối biển", "12000", 3),
        (8, "Bánh quy bơ", "Hộp 150 g · Giòn tan", "28000", 3),
        (9, "Khăn giấy bỏ túi", "Gói 10 tờ · Mềm mại 3 lớp", "6000", 4),
    ]
    with Session(engine) as session, session.begin():
        for number, name, description, amount, category in products:
            product_id = str(UUID(int=number))
            if session.get(ProductRecord, product_id) is None:
                session.add(
                    ProductRecord(
                        id=product_id,
                        name=name,
                        description=description,
                        amount=amount,
                        currency="VND",
                        category_id=str(UUID(int=100 + category)),
                        is_active=True,
                    )
                )
