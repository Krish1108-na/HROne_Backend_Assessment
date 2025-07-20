from fastapi import FastAPI
from routes.product_routes import router as ProductRouter
from routes.order_routes import router as OrderRouter

app = FastAPI()


app.include_router(ProductRouter, prefix="/products", tags=["Products"])
app.include_router(OrderRouter, prefix="/orders", tags=["Orders"])
