var site = function() {
    var changeSection = function(e) {
        e.stopPropagation();

        $(".section").removeClass("active");
        $(".section-nav a").removeClass("active");
        $(this).addClass("active");
        $(".section[name=" + $(this).attr("href").replace("#", "") + "]").addClass("active");
    };

    var formatListItem = function($list) {
        switch($list.attr("name")) {
        case "classes":
            return "<b>" + $list.find("input[name=class-name]").val() + "</b> (" + $list.find("input[name=class-level]").val() + ")";
        }
    };

    var addItem = function(e) {
        e.stopPropagation();
        e.preventDefault();

        var $form = $(this).closest(".input-list").find(".add-item-form");
        $form.addClass("active");
        $form.find("input").val("").first().focus();

        $(".overlay").show();
    };

    var removeItem = function(e) {
        e.stopPropagation();
        e.preventDefault();

        $(this).closest("li").remove();
    };

    var editItem = function(e) {
        e.stopPropagation();
        e.preventDefault();

        var $listItem = $(this).closest("li");
        var $form = $(this).closest(".input-list").find(".add-item-form");
        $listItem.addClass("editing");

        $listItem.find("input").each(function() {
            $form.find("input[name=" + $(this).attr("name") + "]").val($(this).val());
        });

        $form.addClass("active");
        $form.find("input").first().focus();
    };

    var addItemFormHide = function() {
        $(".overlay").hide();
        $(".add-item-form").removeClass("active");
        $("li").removeClass("editing");
    };

    var addItemSubmit = function(elem) {
        var $list = $(elem).closest(".input-list");

        var $listItem = $("li.editing");
        if($listItem.length == 0) {
            $listItem = $("<li />");
        }
        $listItem.empty();

        $("<button />").addClass("remove-item").appendTo($listItem);
        $("<div />").addClass("caption").html(formatListItem($list)).appendTo($listItem);

        $list.find("input").each(function() {
            $("<input />").attr("type", "hidden").attr("name", $(this).attr("name")).val($(this).val()).appendTo($listItem);
        });

        $listItem.appendTo($list.find("ul"));

        addItemFormHide();
    };

    var addItemButtonClick = function(e) {
        e.stopPropagation();
        e.preventDefault();
        addItemSubmit($(this));
    }

    var overlayClick = function(e) {
        e.stopPropagation();
        e.preventDefault();
        addItemFormHide();
    }

    var addItemKeypress = function(e) {
        switch(e.which) {
        case 13:
            e.stopPropagation();
            e.preventDefault();
            addItemSubmit($(this));
            break;
        case 27:
            e.stopPropagation();
            e.preventDefault();
            addItemFormHide($(this));
            break;
        }
    };

    $("body")
        .on("click", "a", changeSection)
        .on("click", "button.add-item", addItem)
        .on("click", "button.remove-item", removeItem)
        .on("click", ".overlay", overlayClick)
        .on("click", ".add-item-form button.save", addItemButtonClick)
        .on("click", ".input-list li", editItem)
        .on("keydown", ".add-item-form", addItemKeypress)
    ;

    if(window.location.hash) {
        $(".section-nav a[href='" + window.location.hash + "']").addClass("active");
        $(".section[name=" + window.location.hash.replace("#", "") + "]").addClass("active");
    }
};

$("document").ready(site);
