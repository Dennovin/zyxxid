var site = function() {
    var spellDetails = {};
    var listData = {};

    var showPopupMessage = function(message) {
        $(".popup-message").html(message).slideDown(200);
        window.setTimeout(function() {
            $(".popup-message").slideUp(200);
        }, 5000);
    };

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
        case "spellclasses":
            return "<b>" + data.name + "</b> (" + data.spellattr.toUpperCase() + ")";
        case "languages":
            return data.name;
        case "abilities":
            return (data.name ? "<b>" + data.name + "</b> - " : "") + data.description;
        case "attacks":
            return "<b>" + data.name + "</b> - " + data.bonus + " - " + data.damage;
        case "resources":
            return data.name;
        case "items":
            if(data.quantity > 1) {
                return "<b>" + data.name + "</b> (" + data.quantity + ")";
            }
            return "<b>" + data.name + "</b>";
        case "spells":
            return "<b>" + data.name + "</b> (" + (data.level == 0 ? "Cantrip" : data.level) + ")";
        case "traits":
            return data;
        }
    };

    var syncList = function(listName) {
        var $list = $(".input-list[name=" + listName + "]");
        $list.find("ul").empty();

        $.each(listData[listName], function(i, data) {
            var $listItem = $("<li />");
            $("<button />").addClass("remove-item").appendTo($listItem);
            $("<div />").addClass("caption").html(formatListItem($list.attr("name"), data)).appendTo($listItem);

            $listItem.appendTo($list.find("ul"));
        });

    };

    var addItem = function(e) {
        e.stopPropagation();
        e.preventDefault();

        var $form = $(this).closest(".input-list").find(".add-item-form");
        $form.addClass("active");
        $form.find("input, textarea, select").val("").first().focus();

        $(".overlay").addClass("adding-item");
    };

    var removeItem = function(e) {
        e.stopPropagation();
        e.preventDefault();

        var listName = $(this).closest(".input-list").attr("name");
        var listIndex = $(this).closest("li").index();
        listData[listName].splice(listIndex, 1);

        syncList(listName);
    };

    var editItem = function(e) {
        e.stopPropagation();
        e.preventDefault();

        var listName = $(this).closest(".input-list").attr("name");
        var $listItem = $(this).closest("li");
        var $form = $(this).closest(".input-list").find(".add-item-form");
        var data = listData[listName][$listItem.index()];

        $listItem.addClass("editing");

        $form.find("input, textarea, select").each(function() {
            $(this).val(data[$(this).attr("name")]);
        });

        $(".overlay").addClass("adding-item");
        $form.addClass("active");
        $form.find("input, textarea").first().focus();
    };

    var addItemFormHide = function() {
        $(".overlay").removeClass("adding-item");
        $(".add-item-form").removeClass("active");
        $("li").removeClass("editing");
    };

    var addItemSubmit = function(elem) {
        var $list = $(elem).closest(".input-list");
        var listName = $list.attr("name")

        var data = {};
        $list.find("input, textarea, select").each(function() {
            if($(this).attr("name") == "") {
                data = $(this).val();
            } else {
                data[$(this).attr("name")] = $(this).val();
            }
        });

        var $listItem = $("li.editing");
        if($listItem.length == 0) {
            listData[listName].push(data);
        } else {
            listData[listName][$listItem.index()] = data;
        }

        syncList(listName);
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

        if(!$(this).hasClass("loading")) {
            addItemFormHide();
            $(".character-list").removeClass("active");
            $(this).removeClass("loading-character");
        }
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
        showPopupMessage("Character saved.");
    };

    var getCharacterJSON = function() {
        var data = {
            name: $(".character-name input").val(),
            character_id: $(".character-id").val()
        };

        $(".input-row input, .input-row textarea, .input-row select").not(".input-list input").each(function() {
            if($(this).attr("type") == "checkbox") {
                if(!data[$(this).attr("name")]) {
                    data[$(this).attr("name")] = 0;
                }
                if(this.checked) {
                    data[$(this).attr("name")]++;
                }
            } else {
                data[$(this).attr("name")] = $(this).val();
            }
        });

        $(".input-list").each(function() {
            data[$(this).attr("name")] = listData[$(this).attr("name")];
        });

        data["spells"] = []
        $(".spell-name.selected").each(function() {
            data["spells"].push($(this).attr("spellid"));
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

        $(".overlay").addClass("loading-character");
        $(".character-list").addClass("active");

        var $list = $(".character-list ul");
        $list.empty();

        $.get("/character").done(function(data) {
            var ids = [];
            for(id in data) {
                ids.push(id);
            }
            var sortedIDs = ids.sort(function(a, b) { return data[a].localeCompare(data[b]); });

            $.each(sortedIDs, function(i, id) {
                var name = data[id];
                var $listItem = $("<li />").attr("characterid", id);
                $("<button />").addClass("remove-item").appendTo($listItem);
                $("<div />").addClass("caption").html(name).appendTo($listItem);

                $listItem.appendTo($(".character-list ul"));
            });
        });
    };

    var loadCharacter = function(id) {
        window.location.hash = id;
        $("body").addClass("loading");
        $.get("/character/" + id).done(function(data) {
            $(".character-name input").val(data["name"]);
            $(".character-id").val(data["character_id"]);

            $(".input-row input, .input-row textarea, .input-row select").not(".input-list input").each(function() {
                if($(this).attr("type") == "checkbox") {
                    $("input[name='" + $(this).attr("name") + "']").slice(0, data[$(this).attr("name")]).attr("checked", true);
                } else {
                    $(this).val(data[$(this).attr("name")]);
                }
            });

            $(".input-list").each(function() {
                var listName = $(this).attr("name");

                listData[listName] = data[listName] || [];
                syncList(listName);
            });

            $.each(data["spells"], function(i, spellid) {
                $(".spell-name[spellid=" + spellid + "]").addClass("selected");
            });

            $(".overlay").removeClass("loading-character");
            $("body").removeClass("loading");
            $(".character-list").removeClass("active");
        });
    };

    var loadCharacterClick = function(e) {
        e.stopPropagation();
        e.preventDefault();

        loadCharacter($(this).closest("li").attr("characterid"));
    };

    var deleteCharacterClick = function(e) {
        e.stopPropagation();
        e.preventDefault();

        $("body").addClass("loading");
        var $listItem = $(this).closest("li");

        $.ajax({url: "/character/" + $listItem.attr("characterid"), type: "DELETE"})
            .done(function(data) {
                $("body").removeClass("loading");
                $listItem.remove();

                var popupMessage = $("<div />").html("Character deleted. ");
                $("<a />").attr({ href: "#", characterid: $listItem.attr("characterid") }).addClass("restore-character").html("Undo").appendTo(popupMessage);
                showPopupMessage(popupMessage);
            });
    };

    var restoreCharacter = function(e) {
        e.stopPropagation();
        e.preventDefault();

        $("body").addClass("loading");

        $.ajax({ type: "POST", url: "/character/undelete/" + $(this).attr("characterid") })
            .done(function(data) {
                loadCharacterList(e);
                showPopupMessage("Undeleted.");
            });
    };

    var requestPDF = function(url) {
        $.get(url).done(function(data, status, jqXHR) {
            if(data.ready) {
                $.fileDownload(data.url);
                $("body").removeClass("loading");
            } else {
                window.setTimeout(function() { requestPDF(url); }, 2000);
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
                requestPDF(data["status_url"]);
            });
        });
    };

    var clearError = function(e) {
        $(this).removeClass("error");
    };

    var showSpellDetails = function(details) {
        $(".spell-details").addClass("loaded");
        $.each(details, function(name, value) {
            if(value.replace) {
                value = value.replace("\n", "<br />").replace(/\*\*(.*?)\*\*/, "<b>$1</b>");
            }

            $(".spell-detail[name=" + name + "]").html(value);
        });
    };

    var loadSpellDetails = function(e) {
        e.stopPropagation();
        e.preventDefault();

        var id = $(this).attr("spellid");
        if(spellDetails[id]) {
            showSpellDetails(spellDetails[id]);
        } else {
            $(".spell-detail").html("");
            $(".spell-details").addClass("loading");
            $.get("/spell/" + id).done(function(data) {
                spellDetails[id] = data;
                showSpellDetails(data);
                $(".spell-details").removeClass("loading");
            });
        }

        $(".spell-name").removeClass("active");
        $(this).addClass("active");
    };

    var redoSpellList = function() {
        $(".spell-name").addClass("untagged");
        $(".spell-tag.selected").each(function() {
            $(".spell-name.spell-tag-" + $(this).attr("value")).removeClass("untagged");
        });
    };

    var toggleCheckbox = function(e) {
        e.stopPropagation();
        e.preventDefault();

        $(this).closest(".checkbox-value").toggleClass("selected");

        if($(this).closest(".checkbox-value").hasClass("spell-tag")) {
            redoSpellList();
        }
    };

    var toggleSpellSection = function(e) {
        e.stopPropagation();
        e.preventDefault();

        $(this).closest(".level-spells").toggleClass("visible");
    };

    $("body")
        .on("click", ".section-nav a", changeSection)
        .on("click", "button.add-item", addItem)
        .on("click", "button.remove-item:not(.character-list button)", removeItem)
        .on("click", ".overlay", overlayClick)
        .on("click", ".add-item-form button.save", addItemButtonClick)
        .on("click", ".input-list li", editItem)
        .on("click", "a.save", saveCharacter)
        .on("click", "a.load", loadCharacterList)
        .on("click", ".character-list li div.caption", loadCharacterClick)
        .on("click", ".character-list li button.remove-item", deleteCharacterClick)
        .on("click", ".restore-character", restoreCharacter)
        .on("click", "a.pdf", generatePDF)
        .on("change", ".error", clearError)
        .on("keydown", ".add-item-form", addItemKeypress)
        .on("click", ".spell-name", loadSpellDetails)
        .on("click", ".checkbox-icon", toggleCheckbox)
        .on("click", ".spell-list .level-header", toggleSpellSection)
    ;

    $(".input-list").each(function() {
        listData[$(this).attr("name")] = [];
    });

    if(window.location.hash) {
        loadCharacter(window.location.hash.replace("#", ""));
    }
};

$("document").ready(site);


var onSignIn = function(googleUser) {
    document.cookie = "googletoken=" + googleUser.getAuthResponse().id_token;
    $("body").addClass("logged-in");
};
