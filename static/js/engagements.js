document.addEventListener("DOMContentLoaded", () => {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie) {
            document.cookie.split(";").forEach(c => {
                const cookie = c.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                }
            });
        }
        return cookieValue;
    }

    const csrftoken = getCookie("csrftoken");


    document.querySelectorAll(".like-btn").forEach(button => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();

            const countSpan = button.querySelector(".count");
            const url = button.dataset.url;
            const count = parseInt(countSpan.innerText) || 0;
            const wasLiked = button.classList.contains("liked");

            button.classList.toggle("liked");
            button.setAttribute('aria-pressed', !wasLiked ? 'true' : 'false');
            countSpan.innerText = wasLiked ? Math.max(0, count - 1) : count + 1;

            try {
                const res = await fetch(url, {
                    method: "POST",
                    headers: { "X-CSRFToken": csrftoken }
                });
                if (!res.ok) throw new Error("Failed");
            } catch (err) {
                button.classList.toggle("liked");
                button.setAttribute('aria-pressed', wasLiked ? 'true' : 'false');
                countSpan.innerText = count;
                console.error(err);
            }
        });
    });


    document.querySelectorAll(".bookmark-btn").forEach(button => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();

            const card = button.closest(".zeph-card");
            const countSpan = button.querySelector(".count");
            const url = button.dataset.url;
            const count = parseInt(countSpan.innerText) || 0;
            const wasBookmarked = button.classList.contains("bookmarked");

            button.classList.toggle("bookmarked");
            button.setAttribute('aria-pressed', !wasBookmarked ? 'true' : 'false');
            countSpan.innerText = wasBookmarked ? Math.max(0, count - 1) : count + 1;

            try {
                const res = await fetch(url, {
                    method: "POST",
                    headers: { "X-CSRFToken": csrftoken }
                });

                if (!res.ok) throw new Error("Failed");


                if (!wasBookmarked === false) {
                    card.style.transition = "opacity 0.2s ease";
                    card.style.opacity = "0";
                    setTimeout(() => card.remove(), 200);
                }

            } catch (err) {
                button.classList.toggle("bookmarked");
                button.setAttribute('aria-pressed', wasBookmarked ? 'true' : 'false');
                countSpan.innerText = count;
                console.error(err);
            }
        });
    });

});

