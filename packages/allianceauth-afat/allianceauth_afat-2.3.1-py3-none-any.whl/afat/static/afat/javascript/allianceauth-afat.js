/**
 * Convert a string to a slug
 * @param {string} text
 * @returns {string}
 */
let convertStringToSlug = function (text) {
    'use strict';

    return text.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-');
};

/**
 * Sorting a table by its first columns alphabetically
 * @param {element} table
 * @param {string} order
 */
let sortTable = function (table, order) {
    'use strict';

    let asc = order === 'asc';
    let tbody = table.find('tbody');

    tbody.find('tr').sort(function (a, b) {
        if (asc) {
            return $('td:first', a).text().localeCompare($('td:first', b).text());
        } else {
            return $('td:first', b).text().localeCompare($('td:first', a).text());
        }
    }).appendTo(tbody);
};

/**
 * Manage a modal window
 * @param {element} modalElement
 */
let manageModal = function (modalElement) {
    'use strict';

    modalElement.on('show.bs.modal', function (event) {
        let modal = $(this);
        let button = $(event.relatedTarget); // Button that triggered the modal
        let url = button.data('url'); // Extract info from data-* attributes
        let cancelText = button.data('cancel-text');
        let confirmText = button.data('confirm-text');
        let bodyText = button.data('body-text');

        let cancelButtonText = modal.find('#cancelButtonDefaultText').text();
        let confirmButtonText = modal.find('#confirmButtonDefaultText').text();

        if (typeof cancelText !== 'undefined' && cancelText !== '') {
            cancelButtonText = cancelText;
        }

        if (typeof confirmText !== 'undefined' && confirmText !== '') {
            confirmButtonText = confirmText;
        }

        modal.find('#cancel-action').text(cancelButtonText);
        modal.find('#confirm-action').text(confirmButtonText);

        modal.find('#confirm-action').attr('href', url);
        modal.find('.modal-body').html(bodyText);
    }).on('hide.bs.modal', function () {
        let modal = $(this);

        modal.find('.modal-body').html('');
        modal.find('#cancel-action').html('');
        modal.find('#confirm-action').html('');
        modal.find('#confirm-action').attr('href', '');
    });
};

/**
 * Prevent double form submits
 */
document.querySelectorAll('form').forEach((form) => {
    'use strict';

    form.addEventListener('submit', (e) => {
        // Prevent if already submitting
        if (form.classList.contains('is-submitting')) {
            e.preventDefault();
        }

        // Add class to hook our visual indicator on
        form.classList.add('is-submitting');
    });
});
