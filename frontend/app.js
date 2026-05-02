const API = "http://localhost:5000";
let token = localStorage.getItem("token") || "";

function authHeaders() {
  return token ? { "Authorization": `Bearer ${token}` } : {};
}

async function request(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
      ...authHeaders()
    }
  });

  if (res.status === 204) return null;

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data.error?.message || `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

async function login() {
  const msg = document.getElementById("loginMessage");
  msg.textContent = "Loading...";
  try {
    const data = await request("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
      })
    });
    token = data.token;
    localStorage.setItem("token", token);
    msg.textContent = `Logged in as ${data.user.email} (${data.user.role})`;
  } catch (err) {
    msg.textContent = `Error: ${err.message}`;
  }
}

async function loadProducts() {
  const box = document.getElementById("products");
  const msg = document.getElementById("productsMessage");
  box.innerHTML = "";
  msg.textContent = "Loading products...";
  try {
    const search = encodeURIComponent(document.getElementById("search").value);
    const data = await request(`/api/v1/products${search ? `?search=${search}` : ""}`);
    msg.textContent = `Success. Cache hit: ${data.cacheHit}`;
    box.innerHTML = data.items.map(p => `
      <div class="product">
        <strong>${p.name}</strong><br>
        ${p.description}<br>
        Price: ${p.price} PLN | Stock: ${p.stock}<br>
        <button onclick="createOrder(${p.id})">Order 1 item</button>
      </div>
    `).join("");
  } catch (err) {
    msg.textContent = `Error: ${err.message}`;
  }
}

async function createProduct() {
  const msg = document.getElementById("adminMessage");
  msg.textContent = "Creating...";
  try {
    await request("/api/v1/products", {
      method: "POST",
      body: JSON.stringify({
        name: document.getElementById("pName").value,
        price: Number(document.getElementById("pPrice").value),
        stock: Number(document.getElementById("pStock").value),
        description: document.getElementById("pDescription").value
      })
    });
    msg.textContent = "Product created.";
    loadProducts();
  } catch (err) {
    msg.textContent = `Error: ${err.message}`;
  }
}

async function createOrder(productId) {
  try {
    await request("/api/v1/orders", {
      method: "POST",
      body: JSON.stringify({ items: [{ productId, quantity: 1 }] })
    });
    alert("Order created");
    loadProducts();
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

async function loadMyOrders() {
  const box = document.getElementById("orders");
  box.innerHTML = "Loading...";
  try {
    const data = await request("/api/v1/orders/my");
    box.innerHTML = data.items.map(o => `
      <div class="order">
        <strong>Order #${o.id}</strong> — ${o.status} — total: ${o.total} PLN
        <ul>${o.items.map(i => `<li>${i.productName}: ${i.quantity} x ${i.unitPrice}</li>`).join("")}</ul>
      </div>
    `).join("") || "No orders yet.";
  } catch (err) {
    box.innerHTML = `Error: ${err.message}`;
  }
}

async function checkHealth() {
  const out = document.getElementById("healthOutput");
  const data = await request("/health");
  out.textContent = JSON.stringify(data, null, 2);
}

async function checkReady() {
  const out = document.getElementById("healthOutput");
  try {
    const data = await request("/ready");
    out.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    out.textContent = `Readiness error: ${err.message}`;
  }
}

loadProducts();
