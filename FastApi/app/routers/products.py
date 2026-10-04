from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
) -> Product:
    product = Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@router.get("", response_model=list[ProductRead])
async def get_all_products(
    db: AsyncSession = Depends(get_db),
) -> list[Product]:
    result = await db.execute(select(Product).order_by(Product.id))
    return result.scalars().all()
