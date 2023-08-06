/* global afatSettings, convertStringToSlug, sortTable, ClipboardJS, manageModal */

$(document).ready(function () {
    'use strict';

    let fatListTable = $('#fleet-edit-fat-list').DataTable({
        ajax: {
            url: afatSettings.url,
            dataSrc: '',
            cache: false
        },
        columns: [
            {data: 'character_name'},
            {data: 'system'},
            {data: 'ship_type'},
            {data: 'actions'}
        ],
        columnDefs: [
            {
                targets: [3],
                orderable: false,
                createdCell: function (td) {
                    $(td).addClass('text-right');
                }
            }
        ],
        order: [
            [0, 'asc']
        ],
        createdRow: function (row, data, rowIndex) {
            let shipTypeOverviewTable = $('#fleet-edit-ship-types');

            let shipTypeSlug = convertStringToSlug(data.ship_type);

            if ($('tr.shiptype-' + shipTypeSlug).length) {
                let currentCount = shipTypeOverviewTable.find(
                    'tr.shiptype-' + shipTypeSlug + ' td.ship-type-count'
                ).html();
                let newCount = parseInt(currentCount) + 1;

                shipTypeOverviewTable.find(
                    'tr.shiptype-' + shipTypeSlug + ' td.ship-type-count'
                ).html(newCount);
            } else {
                shipTypeOverviewTable.append(
                    '<tr class="shiptype-' + shipTypeSlug + '">' +
                    '<td class="ship-type">' + data.ship_type + '</td>' +
                    '<td class="ship-type-count text-right">1</td>' +
                    '</tr>'
                );
            }

            sortTable(shipTypeOverviewTable, 'asc');
        },

        stateSave: true,
        stateDuration: -1
    });

    /**
     * Refresh the datatable information every 15 seconds
     */
    let intervalReloadDatatable = 15000; // ms
    let expectedReloadDatatable = Date.now() + intervalReloadDatatable;

    /**
     * reload datatable "linkListTable"
     */
    let realoadDataTable = function () {
        // the drift (positive for overshooting)
        let dt = Date.now() - expectedReloadDatatable;

        if (dt > intervalReloadDatatable) {
            /**
             * Something really bad happened. Maybe the browser (tab) was inactive?
             * Possibly special handling to avoid futile "catch up" run
             */
            window.location.replace(
                window.location.pathname + window.location.search + window.location.hash
            );
        }

        fatListTable.ajax.reload(
            function (tableData) {
                let shipTypeOverviewTable = $('#fleet-edit-ship-types');
                shipTypeOverviewTable.find('tbody').html('');

                $.each(tableData, function (i, item) {
                    let shipTypeSlug = convertStringToSlug(item.ship_type);

                    if ($('tr.shiptype-' + shipTypeSlug).length) {
                        let currentCount = shipTypeOverviewTable.find(
                            'tr.shiptype-' + shipTypeSlug + ' td.ship-type-count'
                        ).html();
                        let newCount = parseInt(currentCount) + 1;

                        shipTypeOverviewTable.find(
                            'tr.shiptype-' + shipTypeSlug + ' td.ship-type-count'
                        ).html(newCount);
                    } else {
                        shipTypeOverviewTable.append(
                            '<tr class="shiptype-' + shipTypeSlug + '">' +
                            '<td class="ship-type">' + item.ship_type + '</td>' +
                            '<td class="ship-type-count text-right">1</td>' +
                            '</tr>'
                        );
                    }
                });

                sortTable(shipTypeOverviewTable, 'asc');
            },
            false
        );

        expectedReloadDatatable += intervalReloadDatatable;

        // take drift into account
        setTimeout(
            realoadDataTable,
            Math.max(0, intervalReloadDatatable - dt)
        );
    };

    if (afatSettings.reloadDatatable === true) {
        setTimeout(
            realoadDataTable,
            intervalReloadDatatable
        );
    }

    let clipboard = new ClipboardJS('.copy-btn');

    clipboard.on('success', function () {
        $('.copy-btn').tooltip('show');
    });

    /**
     * Modal :: Close ESI fleet
     */
    let cancelEsiFleetModal = $(afatSettings.modal.cancelEsiFleetModal.element);
    manageModal(cancelEsiFleetModal);

    /**
     * Modal :: Delete FAT from FAT link
     */
    let deleteFatModal = $(afatSettings.modal.deleteFatModal.element);
    manageModal(deleteFatModal);

    /**
     * Modal :: Delete FAT from FAT link
     */
    let reopenFatLinkModal = $(afatSettings.modal.reopenFatLinkModal.element);
    manageModal(reopenFatLinkModal);
});
