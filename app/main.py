from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json
import uuid

app = FastAPI()

# In-memory storage for orders (replace with database in production)
orders: Dict[str, Dict] = {}

# Pydantic model for order
class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

class OrderStatusUpdate(BaseModel):
    status: str  # e.g., "pending", "filled", "canceled"

# WebSocket manager to handle connections
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# POST /orders - Submit a new order
@app.post("/orders")
async def create_order(order: OrderCreate):
    order_id = str(uuid.uuid4())
    orders[order_id] = {
        **order.dict(),
        "id": order_id,
        "status": "pending"  # Default status
    }
    await manager.broadcast(json.dumps({
        "event": "order_created",
        "order": orders[order_id]
    }))
    return {"message": "Order created successfully", "order_id": order_id}

# PUT /orders/{order_id}/status - Update order status
@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status_update: OrderStatusUpdate):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    orders[order_id]["status"] = status_update.status
    await manager.broadcast(json.dumps({
        "event": "order_status_updated",
        "order_id": order_id,
        "status": status_update.status
    }))
    return {"message": "Order status updated successfully"}

# GET /orders - Retrieve all orders
@app.get("/orders", response_model=List[dict])
async def get_orders():
    return list(orders.values())

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({"event": "user_disconnected"}))

# Simple HTML page to test WebSocket
@app.get("/")
async def get():
    return """
    <html>
        <head>
            <title>WebSocket Test</title>
        </head>
        <body>
            <h1>WebSocket Test</h1>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
                var ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
                function sendMessage(event) {
                    var input = document.getElementById("messageText");
                    ws.send(input.value);
                    input.value = '';
                    event.preventDefault();
                }
            </script>
        </body>
    </html>
    """