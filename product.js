/**
 * Divine Collection by Verma Jewellers
 * Product Page Logic & Dynamic Hydration
 * Minimalist UI matching exact reference design
 */

(function () {
  "use strict";

  // 1. Get Target Product from URL parameter or pathname
  function getRequestedProduct() {
    const urlParams = new URLSearchParams(window.location.search);
    let id = urlParams.get("id") || urlParams.get("product");

    if (!id) {
      const pathParts = window.location.pathname.split("/").filter(Boolean);
      const lastPart = pathParts[pathParts.length - 1];
      if (lastPart && lastPart !== "product.html" && lastPart !== "index.html") {
        id = lastPart.replace(/\.html$/, "");
      }
    }

    if (id && window.getProductById) {
      const found = window.getProductById(id);
      if (found) return found;
    }

    // Default to first product if none found
    return window.DIVINE_PRODUCTS && window.DIVINE_PRODUCTS.length > 0
      ? window.DIVINE_PRODUCTS[0]
      : null;
  }

  const product = getRequestedProduct();

  if (!product) {
    console.error("Product not found in catalog.");
    return;
  }

  // Set page title & description
  document.title = `${product.title} | Verma Jewellers`;
  const metaDesc = document.querySelector('meta[name="description"]');
  if (metaDesc) {
    metaDesc.setAttribute("content", product.cleanDescription || product.shortDescription);
  }

  // 2. Hydrate Breadcrumbs
  const breadcrumbCurrent = document.getElementById("vj-breadcrumb-current");
  if (breadcrumbCurrent) breadcrumbCurrent.textContent = product.title;

  const breadcrumbCat = document.getElementById("vj-breadcrumb-cat");
  if (breadcrumbCat) breadcrumbCat.textContent = product.category;

  // 3. Hydrate Product Meta Info
  const elTitle = document.getElementById("vj-product-title");
  if (elTitle) elTitle.textContent = product.title;

  const elSku = document.getElementById("vj-product-sku");
  if (elSku) elSku.textContent = `SKU: ${product.sku}`;

  const elNetWeight = document.getElementById("vj-net-weight");
  if (elNetWeight) elNetWeight.textContent = `Net Weight : ${product.netWeight}`;

  const elDesc = document.getElementById("vj-product-desc");
  if (elDesc) elDesc.textContent = product.cleanDescription || product.shortDescription;

  const elPrice = document.getElementById("vj-product-price");
  if (elPrice) elPrice.textContent = product.salePrice;

  // 4. Stock & Shipping Status
  const elStatusBadge = document.getElementById("vj-status-badge");
  const elShippingLead = document.getElementById("vj-shipping-lead");
  const elNotePill = document.getElementById("vj-note-pill");

  if (product.isMakeToOrder) {
    if (elStatusBadge) {
      elStatusBadge.textContent = "MAKE TO ORDER";
      elStatusBadge.className = "vj-status-badge make-to-order";
    }
    if (elShippingLead) {
      elShippingLead.textContent = "EXPECTED DELIVERY WITHIN 20 - 25 WORKING DAYS";
    }
    if (elNotePill) {
      elNotePill.style.display = "inline-block";
    }
  } else {
    if (elStatusBadge) {
      elStatusBadge.textContent = "IN STOCK";
      elStatusBadge.className = "vj-status-badge in-stock";
    }
    if (elShippingLead) {
      elShippingLead.textContent = "EXPECTED SHIPPING WITHIN 5 - 7 WORKING DAYS";
    }
    if (elNotePill) {
      elNotePill.style.display = "none";
    }
  }

  // 5. Color Swatch
  const elColorDot = document.getElementById("vj-color-dot");
  const elColorName = document.getElementById("vj-color-name");
  if (elColorDot) elColorDot.style.background = product.colorHex || "#deb54a";
  if (elColorName) elColorName.textContent = product.colorName || "Yellow";

  // 6. Gallery, Carousel Pagination & Thumbnails
  const mainImg = document.getElementById("vj-main-img");
  const galleryStage = document.getElementById("vj-gallery-stage");
  const thumbStrip = document.getElementById("vj-thumbnails");
  const currentPageEl = document.getElementById("vj-current-page");
  const totalPagesEl = document.getElementById("vj-total-pages");
  const prevBtn = document.getElementById("vj-prev-img");
  const nextBtn = document.getElementById("vj-next-img");

  let productImages = product.images && product.images.length > 0
    ? [...product.images]
    : ["verma_logo.png"];

  // Expand to 4 thumbnails for luxury browsing experience if only 1 or 2 exist
  while (productImages.length < 4 && productImages.length > 0) {
    productImages.push(productImages[productImages.length % 2]);
  }

  let activeImgIndex = 0;

  function setActiveImage(index) {
    if (index < 0) index = productImages.length - 1;
    if (index >= productImages.length) index = 0;
    activeImgIndex = index;

    if (mainImg) {
      mainImg.src = productImages[activeImgIndex];
      mainImg.alt = `${product.title} - View ${activeImgIndex + 1}`;
    }

    if (currentPageEl) currentPageEl.textContent = activeImgIndex + 1;

    // Update thumbnail active border
    document.querySelectorAll(".vj-thumb-box").forEach((thumb, idx) => {
      if (idx === activeImgIndex) {
        thumb.classList.add("active");
      } else {
        thumb.classList.remove("active");
      }
    });
  }

  if (totalPagesEl) totalPagesEl.textContent = productImages.length;

  if (thumbStrip) {
    thumbStrip.innerHTML = "";
    productImages.forEach((imgSrc, idx) => {
      const box = document.createElement("div");
      box.className = `vj-thumb-box ${idx === 0 ? "active" : ""}`;
      box.innerHTML = `<img src="${imgSrc}" alt="Thumbnail ${idx + 1}" loading="lazy">`;
      box.addEventListener("click", () => setActiveImage(idx));
      thumbStrip.appendChild(box);
    });
  }

  if (prevBtn) prevBtn.addEventListener("click", () => setActiveImage(activeImgIndex - 1));
  if (nextBtn) nextBtn.addEventListener("click", () => setActiveImage(activeImgIndex + 1));

  setActiveImage(0);

  // Subtle Smooth Hover Zoom
  if (galleryStage && mainImg) {
    galleryStage.addEventListener("mousemove", (e) => {
      const rect = galleryStage.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      mainImg.style.transformOrigin = `${x}% ${y}%`;
      mainImg.style.transform = "scale(1.55)";
    });

    galleryStage.addEventListener("mouseleave", () => {
      mainImg.style.transform = "scale(1)";
    });
  }

  // Wishlist Heart Toggle
  const wishlistBtn = document.getElementById("vj-wishlist-btn");
  if (wishlistBtn) {
    let isWishlisted = false;
    wishlistBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      isWishlisted = !isWishlisted;
      const heartSvg = wishlistBtn.querySelector("svg");
      if (isWishlisted) {
        heartSvg.style.fill = "#e78287";
        wishlistBtn.style.background = "#fff0f0";
      } else {
        heartSvg.style.fill = "none";
        wishlistBtn.style.background = "#ffffff";
      }
    });
  }

  // 7. WhatsApp & Share Links
  const waBtn = document.getElementById("vj-btn-whatsapp");
  const floatWa = document.getElementById("vj-floating-wa");
  const waMsg = `Namaste Verma Jewellers, I am interested in:\n\n*${product.title}*\nSKU: ${product.sku}\nNet Weight: ${product.netWeight}\nPrice: ${product.salePrice}\n\nPlease share further details and purchase assistance.`;
  const waUrl = `https://api.whatsapp.com/send?phone=919825123456&text=${encodeURIComponent(waMsg)}`;

  if (waBtn) waBtn.href = waUrl;
  if (floatWa) floatWa.href = waUrl;

  const shareBtn = document.getElementById("vj-btn-share");
  if (shareBtn) {
    shareBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (navigator.share) {
        navigator.share({
          title: product.title,
          text: product.cleanDescription,
          url: window.location.href
        }).catch(() => {});
      } else {
        navigator.clipboard.writeText(window.location.href);
        alert("Product link copied to clipboard!");
      }
    });
  }

  // 8. Specifications & Spiritual Tabs
  const specBody = document.getElementById("vj-spec-body");
  if (specBody) {
    const specs = [
      { label: "Product Title", val: product.title },
      { label: "SKU", val: product.sku },
      { label: "Net Weight", val: product.netWeight },
      { label: "Gross Weight", val: product.grossWeight },
      { label: "Gold Karat & Purity", val: product.purity },
      { label: "Stone / Bead Details", val: product.stoneDetails },
      { label: "Dimensions", val: product.dimensions },
      { label: "Hallmarking", val: "BIS 916 Hallmarked with HUID" },
      { label: "Certification", val: "Verma Jewellers Certificate of Authenticity" },
      { label: "Shipping", val: "Free Insured Express Transit" }
    ];
    specBody.innerHTML = specs
      .map((s) => `<tr><th>${s.label}</th><td>${s.val}</td></tr>`)
      .join("");
  }

  const spiritualTitle = document.getElementById("vj-spiritual-title");
  const spiritualText = document.getElementById("vj-spiritual-text");
  const craftText = document.getElementById("vj-craft-text");
  if (spiritualTitle) spiritualTitle.textContent = `Devotional Significance of ${product.theme}`;
  if (spiritualText) spiritualText.textContent = product.spiritualTheme;
  if (craftText) craftText.textContent = product.craftsmanship;

  // Tab switching
  const tabItems = document.querySelectorAll(".vj-tab-item");
  const tabContents = document.querySelectorAll(".vj-tab-content");
  tabItems.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabItems.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));
      btn.classList.add("active");
      const target = btn.getAttribute("data-tab");
      const targetEl = document.getElementById(target);
      if (targetEl) targetEl.classList.add("active");
    });
  });

  // 9. Related Products Grid
  const relatedGrid = document.getElementById("vj-related-grid");
  if (relatedGrid && product.relatedHandles && window.DIVINE_PRODUCTS) {
    const items = product.relatedHandles
      .map((h) => window.getProductById(h))
      .filter(Boolean);

    relatedGrid.innerHTML = items
      .map(
        (item) => `
      <a href="product.html?id=${item.handle}" class="vj-rel-card">
        <div class="vj-rel-img">
          <img src="${item.images[0]}" alt="${item.title}" loading="lazy">
        </div>
        <div class="vj-rel-info">
          <div style="font-size: 11px; color: var(--vj-text-muted); text-transform: uppercase;">${item.sku}</div>
          <h4 class="vj-rel-title">${item.title}</h4>
          <div class="vj-rel-price">${item.salePrice}</div>
        </div>
      </a>
    `
      )
      .join("");
  }

  // 10. Cart Drawer Logic
  let cart = JSON.parse(localStorage.getItem("vj_cart") || "[]");

  function updateCart() {
    const badge = document.getElementById("vj-cart-badge");
    const count = cart.reduce((sum, item) => sum + item.qty, 0);
    if (badge) badge.textContent = count;

    const itemsWrap = document.getElementById("vj-cart-items");
    const subtotalEl = document.getElementById("vj-cart-subtotal");

    if (itemsWrap) {
      if (cart.length === 0) {
        itemsWrap.innerHTML = `<p style="text-align: center; color: #888; margin-top: 40px; font-size: 13px;">Your shopping bag is empty.</p>`;
      } else {
        itemsWrap.innerHTML = cart
          .map(
            (it, i) => `
          <div class="vj-cart-item">
            <img class="vj-cart-item-img" src="${it.img}" alt="${it.title}">
            <div class="vj-cart-item-info">
              <div class="vj-cart-item-title">${it.title}</div>
              <div style="font-size: 11px; color: #999;">Qty: ${it.qty}</div>
              <div class="vj-cart-item-price">${it.price}</div>
            </div>
            <button class="vj-cart-remove" data-idx="${i}" style="background:none; border:none; color:#c0392b; cursor:pointer; font-size:16px;">✕</button>
          </div>
        `
          )
          .join("");

        document.querySelectorAll(".vj-cart-remove").forEach((b) => {
          b.addEventListener("click", (e) => {
            const idx = parseInt(e.target.getAttribute("data-idx"));
            cart.splice(idx, 1);
            localStorage.setItem("vj_cart", JSON.stringify(cart));
            updateCart();
          });
        });
      }
    }

    if (subtotalEl) {
      const total = cart.reduce((sum, it) => sum + it.priceNum * it.qty, 0);
      subtotalEl.textContent = `₹${total.toLocaleString("en-IN")}.00`;
    }
  }

  updateCart();

  const cartOverlay = document.getElementById("vj-cart-overlay");
  const cartBtn = document.getElementById("vj-header-cart-btn");
  const cartClose = document.getElementById("vj-cart-close-btn");

  if (cartBtn && cartOverlay) {
    cartBtn.addEventListener("click", (e) => {
      e.preventDefault();
      cartOverlay.classList.add("open");
    });
  }
  if (cartClose && cartOverlay) {
    cartClose.addEventListener("click", () => cartOverlay.classList.remove("open"));
  }
  if (cartOverlay) {
    cartOverlay.addEventListener("click", (e) => {
      if (e.target === cartOverlay) cartOverlay.classList.remove("open");
    });
  }

  // Add to Cart
  const atcBtn = document.getElementById("vj-btn-atc");
  if (atcBtn) {
    atcBtn.addEventListener("click", () => {
      const existing = cart.find((it) => it.id === product.id);
      if (existing) {
        existing.qty += 1;
      } else {
        cart.push({
          id: product.id,
          title: product.title,
          price: product.salePrice,
          priceNum: product.salePriceNum,
          img: product.images[0],
          qty: 1
        });
      }
      localStorage.setItem("vj_cart", JSON.stringify(cart));
      updateCart();
      if (cartOverlay) cartOverlay.classList.add("open");
    });
  }

  // Buy It Now
  const buyBtn = document.getElementById("vj-btn-buy");
  if (buyBtn) {
    buyBtn.addEventListener("click", () => {
      atcBtn.click();
    });
  }
})();
