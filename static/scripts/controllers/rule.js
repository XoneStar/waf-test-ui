'use strict';

/**
 * @ngdoc function
 * @name composeUiApp.controller:ProjectCtrl
 * @description
 * # ProjectCtrl
 * Controller of the composeUiApp
 */
angular.module('WafUiApp')
    .controller('RuleCtrl', function ($scope, $routeParams) {
        $scope.id = $routeParams.id;
        $scope.title = $routeParams.title;
    });