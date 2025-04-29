function reveal() {
    var sections = document.querySelectorAll("section");

    sections.forEach(function(section) {
        var windowHeight = window.innerHeight;
        var elementTop = section.getBoundingClientRect().top;
        var elementVisible = 150;

        if (elementTop < windowHeight - elementVisible) {
            section.classList.add("shown");
        } else {
            section.classList.remove("shown");
        }});}

window.addEventListener("scroll", function() {
    reveal();
});
