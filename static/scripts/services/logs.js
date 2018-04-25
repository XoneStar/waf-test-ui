'use strict';

angular.module('WafUiApp')
    .factory('logService', function () {

        function sortByDate(data) {
            return data.sort(function (a, b) {
                if (a.text < b.text) {
                    return -1;
                } else if (a.text > b.text) {
                    return 1;
                } else {
                    return 0;
                }
            });
        }

        function excludeBlankLines(lines) {
            return _.filter(lines, function (line) {
                return line.text.trim().length > 0;
            });
        }

        var formatLogs = _.flowRight(
            sortByDate,
            excludeBlankLines,
            _.flatten);

        return {
            formatLogs: formatLogs
        };
    });