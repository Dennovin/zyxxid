var site = function() {
    $(".section-nav").on("click", "a", function(e) {
        e.stopPropagation();

        $(".section").removeClass("active");
        $(".section-nav a").removeClass("active");
        $(this).addClass("active");
        $(".section[name=" + $(this).attr("href").replace("#", "") + "]").addClass("active");
    });

    if(window.location.hash) {
        $(".section-nav a[href='" + window.location.hash + "']").addClass("active");
        $(".section[name=" + window.location.hash.replace("#", "") + "]").addClass("active");
    }
};

$("document").ready(site);
