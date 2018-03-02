'use strict';

/**
 * @ngdoc function
 * @name composeUiApp.controller:CreateCtrl
 * @description
 * # CreateCtrl
 * Controller of the composeUiApp
 */
angular.module('WafUiApp')
    .controller('CreateCtrl', function ($scope, $routeParams, $resource, $location) {

        var Rule = $resource('api/v1/rules', null, {
            'createRule': {
                url: 'api/v1/add',
                method: 'POST'
            },
            'updateUrl': {
                url: 'api/v1/modify',
                method: 'POST'
            }
        });

        $scope.createRule = function (title, naxsi_core, naxsi) {

            //TODO: check if name is alphanumeric
            Rule.createRule({
                title: title,
                naxsi_core: naxsi_core,
                naxsi: naxsi
            }, function (data) {
                if ('0' === data.status) {
                    alertify.success('添加成功');
                    $scope.$parent.reload(false);
                    $location.path('/');
                } else {
                    alertify.error(data.message);
                }

            }, function (err) {
                alertify.alert(err.data);
            });


        };

        // update url
        $scope.updateUrl = function (url) {

            Rule.updateUrl({url: url}, function (data) {
                alertify.alert(data.message);
            }, function (err) {
                alertify.alert(err.data);
            });

        };

    });
