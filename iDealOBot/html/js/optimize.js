function moveStylesheetsToHead() {
    const stylesheets = document.querySelectorAll('link[rel="stylesheet"]');
    stylesheets.forEach(stylesheet => {
        if (stylesheet.parentElement.tagName !== 'HEAD') {
            const stylesheetID = stylesheet.id;
            if (!stylesheetID || !document.querySelector(`head #${stylesheetID}`)) {
                document.head.prepend(stylesheet);
            } else {
                stylesheet.remove();
            }
        }
    });
}

function lightspeedOptimizeFlat(styleSheetElement) {
    if (document.querySelectorAll('link[href*="thrive_flat.css"]').length > 1) {
        styleSheetElement.setAttribute('disabled', true);
    } else if (styleSheetElement.parentElement.tagName !== 'HEAD') {
        document.head.append(styleSheetElement);
    }
}

window.lightspeedOptimizeFlat = lightspeedOptimizeFlat;
document.addEventListener('DOMContentLoaded', moveStylesheetsToHead);