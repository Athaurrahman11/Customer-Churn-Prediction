const navToggle = document.getElementById("navToggle");
const navLinks  = document.getElementById("navLinks");

if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
        const isOpen = navLinks.classList.toggle("open");
        navToggle.setAttribute("aria-expanded", isOpen);
    });

    navLinks.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("open");
            navToggle.setAttribute("aria-expanded", "false");
        });
    });

    document.addEventListener("click", (e) => {
        if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove("open");
            navToggle.setAttribute("aria-expanded", "false");
        }
    });
}

const form      = document.getElementById("predictionForm");
const submitBtn = document.getElementById("submitBtn");

if (form && submitBtn) {
    form.addEventListener("submit", (e) => {
        if (!form.checkValidity()) {
            form.reportValidity();
            e.preventDefault();
            return;
        }
        submitBtn.classList.add("loading");
        submitBtn.disabled = true;
    });
}

const resultPanel = document.getElementById("resultPanel");

if (resultPanel) {
    setTimeout(() => {
        resultPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 120);
}

const sections = document.querySelectorAll("section[id]");
const navItems = document.querySelectorAll(".nav-link");

if (sections.length && navItems.length) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navItems.forEach(link => {
                    link.classList.remove("active");
                    if (link.getAttribute("href") === "#" + id) {
                        link.classList.add("active");
                    }
                });
            }
        });
    }, { rootMargin: "-20% 0px -60% 0px" });

    sections.forEach(section => observer.observe(section));
}
