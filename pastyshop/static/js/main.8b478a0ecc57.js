$(document).ready(function() {
    // Initialize the carousel
    $("#carouselExampleSlidesOnly").carousel();

    // Stop automatic sliding on hover
    $("#carouselExampleSlidesOnly").hover(
        function() {
            $(this).carousel("pause");
        },
        function() {
            $(this).carousel("cycle");
        }
    );
});
