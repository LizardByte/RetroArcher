let translations = null

let getTranslation = function(string) {
    // download translations
    if (translations === null) {
        $.ajax({
            async: false,
            url: "/translations/",
            type: "GET",
            dataType: "json",
            success: function (result) {
                translations = result
            }
        })
    }

    if (translations) {
        try {
            if (translations[string]) {
                return translations[string]
            } else {
                return string
            }
        } catch (err) {
            return string
        }
    }
    else {
        // could not download translations
        return string
    }
}
