'use strict';

/**
 * @ngdoc function
 * @name composeUiApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the composeUiApp
 */
angular.module('WafUiApp')
    .controller('MainCtrl', function ($scope, $resource, pageSize) {

        var urls = $resource('api/v1/rules');

        function reload(displayMessage) {
            urls.get(function (data) {
                $scope.rules = data;
                if (displayMessage) {
                    alertify.success(Object.keys(data.rules).length + ' rules reloaded');
                }
            });
        }

        $scope.reload = reload;

        $scope.isEmpty = function (obj) {
            return angular.equals({}, obj);
        };

        $scope.page = 0;
        $scope.pageSize = pageSize;

        $scope.size = function (rules) {
            return rules ? Object.keys(rules).length : 0;
        };


        reload(false);

    });
