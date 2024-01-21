// create alert placeholder container
let alert_placeholder = document.createElement('div');
alert_placeholder.id = 'alert_placeholder';
alert_placeholder.className = 'container alert_placeholder';
document.body.appendChild(alert_placeholder);

function showAlert(message, alert_type = 'alert-info', icon_class = null, timeout = null) {
    // get current timestamp
    let now = Date.now()

    // create the alert div
    let alert_div = document.createElement('div');
    alert_div.id = `alert_div_${now}`;
    alert_div.className = `alert ${alert_type} alert-dismissible fade show`;
    alert_div.setAttribute('role', 'alert');
    alert_div.textContent = message;

    // create the icon and prepend it to the message
    if (icon_class !== null) {
        let icon = document.createElement('i');
        icon.className = icon_class;
        alert_div.prepend(icon);
    }

    // create the alert close button
    let alert_close = document.createElement('button');
    alert_close.type = 'button';
    alert_close.className = 'btn-close';
    alert_close.setAttribute('data-bs-dismiss', 'alert');
    alert_close.setAttribute('aria-label', 'Close');

    // append the elements to the placeholder
    alert_div.appendChild(alert_close);
    alert_placeholder.appendChild(alert_div);

    // close alert after timeout
    if (timeout !== null) {
        setTimeout(function () {
            $(`#alert_div_${now}`).remove();
        }, timeout);
    }
}
