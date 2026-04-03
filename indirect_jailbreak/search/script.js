document.addEventListener("DOMContentLoaded", (e) => {
    let clickable = document.getElementById("clickable");
    clickable.addEventListener('click', function(event) {
        window.location.href = "https://hongjangyang.shop/__BLOG_PATH__/index.html?__BLOG_KEY__=_PLACEHOLDER_"
    });
});