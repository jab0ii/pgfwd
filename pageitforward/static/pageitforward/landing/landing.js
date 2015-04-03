'use strict';

angular.module('PageItForwardApp.Landing', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/landing', {
    templateUrl: 'Landing/landing.html',
    controller: 'View1Ctrl'
  });
}])

.controller('LandingCtrl', [function() {

}]);


angular.module('UserValidation', []).directive('validPasswordC', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (viewValue, $scope) {
                var noMatch = viewValue != scope.myForm.password.$viewValue
                ctrl.$setValidity('noMatch', !noMatch)
            })
        }
    }
})

PageItForwardApp.controller('LandingCtlr', ['$scope', '$http', '$location', function($scope, $http, $location) {
    $scope.submit = function(user) {
        $http.post('/API/login', user).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                console.log(data);
//                var orgName = data['org']['orgName'];
//                $http.get('/')

                $location.url('/postLogin');
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                console.log("ERRORZZZZZ");
              });
        };

    $scope.registerSubmit = function(formData) {
        $http.post('/API/users', formData).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                console.log(data);
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                console.log("ERRORZZZZZ");
              });
        };
}]);