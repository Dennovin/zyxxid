var site = function() {
    var changeSection = function(e) {
        e.stopPropagation();
        e.preventDefault();

        $(".section").removeClass("active");
        $(".section-nav a").removeClass("active");
        $(this).addClass("active");
        $(".section[name=" + $(this).attr("name") + "]").addClass("active");
    };

    var formatListItem = function(listName, data) {
        switch(listName) {
        case "classes":
            return "<b>" + data.name + "</b> (" + data.level + ")";
        case "abilities":
            return data.name;
        case "attacks":
            return data.name;
        case "resources":
            return data.name;
        case "items":
            if(data.quantity > 1) {
                return "<b>" + data.name + "</b> (" + data.quantity + ")";
            }
            return "<b>" + data.name + "</b>";
        case "spells":
            return "<b>" + data.name + "</b> (" + (data.level == 0 ? "Cantrip" : data.level) + ")";
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

        $(".overlay").show();
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

        var data = {};
        $list.find("input").each(function() {
            data[$(this).attr("name")] = $(this).val();
        });

        $("<div />").addClass("caption").html(formatListItem($list.attr("name"), data)).appendTo($listItem);
        $.each(data, function(name, value) {
            $("<input />").attr("type", "hidden").attr("name", name).val(value).appendTo($listItem);
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
        $(".character-list").removeClass("active");
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

    var saveSuccess = function(data) {
        $(".character-id").val(data["id"]);
        window.location.hash = data["id"];
    };

    var getCharacterJSON = function() {
        var data = {
            name: $(".character-name input").val(),
            character_id: $(".character-id").val()
        };

        $(".input-row input").not(".input-list input").each(function() {
            data[$(this).attr("name")] = $(this).val();
        });

        $(".input-list").each(function() {
            list = data[$(this).attr("name")] = [];
            $(this).find("li").each(function() {
                var itemData = {};
                $(this).find("input").each(function() {
                    itemData[$(this).attr("name")] = $(this).val();
                });
                list.push(itemData);
            });
        });

        return JSON.stringify(data);
    };

    var saveCharacter = function(e) {
        e.stopPropagation();
        e.preventDefault();

        if(!$(".character-name input").val()) {
            $(".character-name input").addClass("error");
            return;
        }

        $.ajax({
            type: "POST",
            url: "/character",
            data: getCharacterJSON(),
            headers: {
                "Content-Type": "application/json"
            }
        }).done(saveSuccess);
    };

    var loadCharacterList = function(e) {
        e.stopPropagation();
        e.preventDefault();

        $(".overlay").show();
        $(".character-list").addClass("active");

        var $list = $(".character-list ul");
        $list.empty();

        $.get("/character").done(function(data) {
            $.each(data, function(id, name) {
                $("<li />").attr("id", id).html(name).appendTo($list);
            });
        });
    };

    var loadCharacter = function(id) {
        window.location.hash = id;
        $.get("/character/" + id).done(function(data) {
            $(".character-name input").val(data["name"]);
            $(".character-id").val(data["character_id"]);

            $(".input-row input").not(".input-list input").each(function() {
                $(this).val(data[$(this).attr("name")]);
            });

            $(".input-list").each(function() {
                var $list = $(this);
                $list.find("ul").empty();

                $.each(data[$(this).attr("name")], function(i, row) {
                    var $listItem = $("<li />");

                    $("<button />").addClass("remove-item").appendTo($listItem);
                    $("<div />").addClass("caption").html(formatListItem($list.attr("name"), row)).appendTo($listItem);

                    $list.find("input").each(function() {
                        $("<input />").attr("type", "hidden").attr("name", $(this).attr("name")).val(row[$(this).attr("name")]).appendTo($listItem);
                    });

                    $listItem.appendTo($list.find("ul"));
                });

                list = data[$(this).attr("name")] = [];
                $(this).find("li").each(function() {
                    var itemData = {};
                    $(this).find("input").each(function() {
                        itemData[$(this).attr("name")] = $(this).val();
                    });
                    list.push(itemData);
                });
            });

            $(".overlay").hide();
        });
    };

    var loadCharacterClick = function(e) {
        e.stopPropagation();
        e.preventDefault();

        loadCharacter($(this).attr("id"));
    };

    var requestPDF = function(url) {
        $.get(url).done(function(data, status, jqXHR) {
            if(jqXHR.status == 202) {
                window.setTimeout(function() { requestPDF(url); }, 2000);
            } else {
                console.log(data);
            }
        });
    };

    var generatePDF = function(e) {
        e.stopPropagation();
        e.preventDefault();

        $("body").addClass("loading");

        if(!$(".character-name input").val()) {
            $(".character-name input").addClass("error");
            return;
        }

        $.ajax({
            type: "POST",
            url: "/character",
            data: getCharacterJSON(),
            headers: {
                "Content-Type": "application/json"
            }
        }).done(function(data) {
            $(".character-id").val(data["id"]);
            window.location.hash = data["id"];
            $.ajax({
                type: "POST",
                url: "/pdf",
                data: {"character_id": data["id"]}
            }).done(function(data) {
                $.get(data["status_url"])
                    .done(function(data) {
                        console.log(data);
                    });
                $("<a />").attr("href", data["status_url"]).attr("download", data["filename"]).click();
            });
        });
    };

    var clearError = function(e) {
        $(this).removeClass("error");
    };

    $("body")
        .on("click", ".section-nav a", changeSection)
        .on("click", "button.add-item", addItem)
        .on("click", "button.remove-item", removeItem)
        .on("click", ".overlay", overlayClick)
        .on("click", ".add-item-form button.save", addItemButtonClick)
        .on("click", ".input-list li", editItem)
        .on("click", "a.save", saveCharacter)
        .on("click", "a.load", loadCharacterList)
        .on("click", ".character-list li", loadCharacterClick)
        .on("click", "a.pdf", generatePDF)
        .on("change", ".error", clearError)
        .on("keydown", ".add-item-form", addItemKeypress)
    ;

    if(window.location.hash) {
        loadCharacter(window.location.hash.replace("#", ""));
    }
};

$("document").ready(site);


var onSignIn = function(googleUser) {
    document.cookie = "googletoken=" + googleUser.getAuthResponse().id_token;
};

