'use strict';

/**
 * @ngdoc overview
 * @name composeUiApp
 * @description
 * # composeUiApp
 *
 * Main module of the application.
 */
angular
    .module('WafUiApp', [
        'ngResource',
        'ngRoute'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/home.html',
                controller: 'HomeCtrl'
            })
            .when('/rule/:id/:title', {
                templateUrl: 'views/rule.html',
                controller: 'RuleCtrl'
            })
            .when('/create', {
                templateUrl: 'views/create.html',
                controller: 'CreateCtrl'
            })
            .when('/create/:from', {
                templateUrl: 'views/create.html',
                controller: 'CreateCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    });
