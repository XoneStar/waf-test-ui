'use strict';

angular.module('WafUiApp')
    .config(function ($sceDelegateProvider) {

    })
    .directive('edit', function ($resource, $log, $window, $location) {
        return {
            restrict: 'E',
            templateUrl: 'views/edit.html',
            controller: function ($scope) {

                $scope.isShow = false;
                var Rule = $resource('api/v1/get/' + $scope.id, null, {});

                var Conf = $resource('api/v1/getURL/', null, {});

                var Url = $resource('api/v1/modify', null, {});

                var Update = $resource('api/v1/update', null, {});

                var Delete = $resource('api/v1/removeRule', null, {});

                $scope.$watch('id', function (val) {
                    if (val) {

                    }

                });

                $scope.isEmpty = function (obj) {
                    return angular.equals({}, obj);
                };

                $scope.details = function () {
                    $scope.isShow = true;
                    Rule.get(function (data) {
                        $scope.uuid = data.uuid;
                        $scope.title = data.title;
                        $scope.naxsi_core = data.naxsi_core;
                        $scope.naxsi = data.naxsi;
                    });

                    Conf.get(function (data) {
                        $scope.url = data.url;
                    })

                };

                $scope.showDailog = function () {
                    alertify.prompt('防护地址修改：', $scope.url, function (evt, url) {

                        if (url !== '') {
                            Url.save({"url": url}, function (data) {
                                alertify.success(data.message);
                                if ('成功' === data.message) {
                                    $scope.url = url
                                }
                            });
                        }
                    });
                };

                $scope.updateRule = function (naxsi_core, naxsi) {
                    Update.save({"uuid": $scope.id, "naxsi_core": naxsi_core, "naxsi": naxsi}, function (data) {
                        alertify.success(data.message)
                    })
                };

                $scope.deleteRule = function (id) {
                    alertify.confirm('你确定要删除这条规则?', function (rm) {
                        if (rm) {
                            Delete.save({"uuid": id}, function (data) {
                                if ('0' === data.status) {
                                    alertify.message('成功删除' + id);
                                    $scope.$parent.reload(false);
                                    $location.path('/');
                                } else {
                                    alertify.message(data.message);
                                }
                            });
                        }
                    });
                };
            }
        };
    });