document.addEventListener("DOMContentLoaded", (e) => {
    let textarea = document.getElementById("textarea");
    textarea.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // 줄바꿈 차단
            window.location.href = "https://hongjangyang.shop/search/index.html?q=ethernet"
        }
    });
});