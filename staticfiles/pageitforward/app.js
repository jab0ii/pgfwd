'use strict';

// Author: Jaspreet Singh

// Declare app level module which depends on views, and components
// pre-loads ngRoute UserValidation as dependencies
var PageItForwardApp = angular.module('PageItForwardApp', [
  'ngRoute', 'UserValidation', 'ngStorage'
]).config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';    }
]);

//additional config for route handling
PageItForwardApp.config(function($routeProvider) {
    $routeProvider

        // route for the home page
        .when('/', {
            templateUrl: '/static/pageitforward/landing/landing.html',
//            templateUrl: '/templates/pageitforward/landing.html',
            controller: 'LandingCtlr'
        })
        
        // route to signup page
        .when('/signup', {templateUrl: '/static/pageitforward/landing/signup.html',
            controller: 'LandingCtlr'
        })

        // route for the profile page
        .when('/profile', {
            templateUrl: '/static/pageitforward/profile/profile.html',
            controller: 'LandingCtlr'
        })

        // route for the log out and back to home page
        .when('/logout', {
            templateUrl: '/static/pageitforward/landing/landing.html',
            controller: 'LandingCtlr'
        })

        // route for associating a user with org
        .when('/associateUser', {
            templateUrl: '/static/pageitforward/associateUser/associateUser.html',
            controller: 'LandingCtlr'
        })

        // route for the create org page
        .when('/createOrg', {
            templateUrl: '/static/pageitforward/createOrg/createOrg.html',
            controller: 'LandingCtlr'
        })

        // route for the create org page
        .when('/createEvent', {
            templateUrl: '/static/pageitforward/createEvent/createEvent.html',
            controller: 'LandingCtlr'
        })

        // route for the profile page
        .when('/createEventHandler', {
            templateUrl: '/static/pageitforward/createEventHandler/createEventHandler.html',
            controller: 'LandingCtlr'
        })
        
        .when('/getLogEvent', {
            templateUrl: '/static/pageitforward/dashBoard.html',
            controller: 'LandingCtlr'
        })
});

//declaring uservalidation module, this is the module that allows us to do validation for the signup page
angular.module('UserValidation', []).directive('validPasswordC', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (viewValue, $scope) {
                var noMatch = viewValue != scope.myForm.password.$viewValue;
                ctrl.$setValidity('noMatch', !noMatch)
            })
        }
    }
});

//landing page controller, declares dependencies (scope, http, and location)
PageItForwardApp.controller('LandingCtlr', ['$scope', '$http', '$location', '$compile', function($scope, $http, $location, $compile, $localStorage, $sessionStorage) {

    $scope.$storage = $localStorage;

    $scope.noInputError = true;

    $scope.$watch(window.localStorage.getItem("PIFloggedIn"),
        function(newValue, oldValue){
//            console.log("PIFloggedIn changed from " + oldValue + " to " + newValue);
            $scope.loggedIn = newValue;
        }
    );

    $scope.$watch(window.localStorage.getItem("PIFuserName"),
        function(newValue, oldValue){
//            console.log("PIFusername CHANGED!");
            $scope.user = window.localStorage.getItem("PIFuserName");
        }
    );

    $scope.$watch(window.localStorage.getItem("PIFhasOrg"),
        function(newValue, oldValue){
//            console.log("PIFhasOrg CHANGED!");
            $scope.hasOrg = window.localStorage.getItem("PIFhasOrg");
        }
    );

    $scope.$watch(window.localStorage.getItem("PIForgName"),
        function(newValue, oldValue){
            if(typeof window.localStorage.getItem("PIForgName") == 'string') {
                $scope.orgName = window.localStorage.getItem("PIForgName");
            }
        }
    );



    //function fixes the scrolling carousel
    $scope.scrollLeft = function(){
        console.log("scrolling left");
        $('#landingCarousel').carousel('prev');
    };

    //function fixes the scrolling carousel
    $scope.scrollRight = function(){
        console.log("scrolling right");
        $('#landingCarousel').carousel('next');
    };

    //function moves us to different URL
    $scope.changeView = function(view) {
            $location.url(view);
    };
    
    $scope.signUp = function(){
            $location.url('/signup');

    }

    $scope.sendEvent = function(){
        var postData = {};
        var handlerSelection = angular.element(document.querySelector('#eventHandlerSelection'));
        var eventTitle = angular.element(document.querySelector('#eventTitle')).val();
        var eventMessage = angular.element(document.querySelector('#eventMessage')).val();
        var eventAPIKey = window.localStorage.getItem("PIFapiKey");
        var eventDetailJSON = {};
        var failEl = angular.element(document.querySelector('#eventCreateFail'));
        var successEl = angular.element(document.querySelector('#eventCreateSuccess'));
        handlerSelection = handlerSelection[0].options[handlerSelection[0].selectedIndex].value;
        postData['handler'] = handlerSelection;
        postData['apiKey'] = eventAPIKey;
        eventDetailJSON['title'] = eventTitle;
        eventDetailJSON['message'] = eventMessage;
        postData['eventDetails'] = eventDetailJSON;
        console.log(postData);
        $http.post('/API/createEvent', postData).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                console.log("Got success from API endpoint");
                console.log("RESPONSE:");
                if(data['success'] == false){
                    failEl.removeClass('hide');
                }
                else{
                    successEl.removeClass('hide');
                }
                console.log(data);
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              });
    };

    $scope.createEvent = function(){
       console.log("Calling API");
       $http.get('/API/eventhandlers').
          success(function(data, status, headers, config) {
            // this callback will be called asynchronously
            // when the response is available
            console.log("Got success from GET event handlers API");
            console.log("RESPONSE:");
            console.log(data);
            console.log("This should be an array of event handlers");
            console.log(data['eventHandlers']);
            $scope.eventHandlers = data['eventHandlers'];
          }).
          error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });
        $scope.changeView('/createEvent');
    };

    $scope.postEventHandler = function(){
        var postData = {};
        var EventHandlerTitle = angular.element(document.querySelector('#EventHandlerTitle'));
        EventHandlerTitle = EventHandlerTitle.find("input");

        postData['title'] = EventHandlerTitle.val();

        var hierarchyData = {};

        var numTimers = angular.element(document.querySelectorAll('.timerValue'));
        console.log(numTimers);
        console.log("Number of levels (timer values): " + numTimers.size());

        hierarchyData['numLevels'] = numTimers.size();
        hierarchyData['levels'] = {};

        for(var i = 0; i < numTimers.size(); i++){
            var levelData = {};
            console.log("Processing level " + i);
            var timerEl = numTimers[i];
            if(timerEl.childNodes.length == 5){
                var timerIn = timerEl.childNodes[3];
            }
            else{
                var timerIn = timerEl.childNodes[1];
            }
            levelData["timeout"] = parseInt(timerIn.value);

            var siblingEl = timerEl.nextElementSibling;
            var users = [];
            while(siblingEl != null){

                if('className' in siblingEl && siblingEl.className == 'timerValue ng-scope'){
                    break;
                }

                if('className' in siblingEl &&
                    (siblingEl.className == 'userSelect'
                        || siblingEl.className == 'userSelect ng-scope')){
//                    console.log("found user select");
                    var childNodes = siblingEl.childNodes;
//                    console.log(childNodes.length);
                    if(childNodes.length == 2){
                        var selectEl = childNodes[1];
                        console.log(selectEl);
                        users.push(parseInt(selectEl.options[selectEl.selectedIndex].value));
                    }
                    if(childNodes.length==5){
                        var selectEl = childNodes[3];
                        users.push(parseInt(selectEl.options[selectEl.selectedIndex].value));
                    }

                }
                siblingEl = siblingEl.nextElementSibling;
            }
            levelData['users'] = users;
            hierarchyData['levels'][String(i)] = levelData;
        }

        postData['hierarchy'] = hierarchyData;
        console.log(postData);

        $http.post('/API/eventhandlers', postData).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                console.log("Got success from API endpoint");
                console.log("RESPONSE:");
                console.log(data);
                var successEl = angular.element(document.querySelector('#eventHandlerCreateSuccess'));
                successEl.removeClass('hide');
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              });


    };

    $scope.getLogEvent = function() {
        var orgID = window.localStorage.getItem('PIForgID');
        console.log("logevent bitches");
        if (orgID == null) {
            console.log("shit ball, must have org");
        }
        else {
            $http.get('/API/getLogEvent').
                success(function(date, status, headers, config) {
                    console.log("got some shit from logevent");
                    console.log(data);
                    $scope.logeventData = data['logEvents'];
                    $location.url('/getLogEvent');

                    
            }).error(function(data, status, headers, config){
                   console.log("error calling api/getlogevents");
                });
        }

    };
    $scope.createEventHandler = function(){
        var orgID = window.localStorage.getItem('PIForgID');
        console.log("createEventHandler was called");
        if(orgID == null){
            console.log("User trying to go to create event handler page without being associated");
        }
        else{
            $http.get('/API/orgUsers/'+orgID).
                success(function(data, status, headers, config){
                    console.log("Got response from API");
                    console.log(data);
                    $scope.users = data['users'];
                    $scope.changeView('/createEventHandler');

                }).
                error(function(data, status, headers, config){
                   console.log("error calling api/orgusers");
                });
        }
    };


    $scope.addUserOption = function(){
        console.log("Adding user option");
        var formDiv = angular.element(document.querySelector('#CreateEventForm'));

        var template = '<div class="userSelect"><label>Select User: </label><select><option ng-repeat="user in users" value="{{ user.id }}">{{ user.firstName }} {{ user.lastName }}</option></select></div>';
        var compiled = $compile(template)($scope);
        console.log("compiled");
        formDiv.append(compiled);
        console.log("appending");
    };

    $scope.addEventHandlerLevel = function(){
        console.log("Adding Event Handler Level");
        var formDiv = angular.element(document.querySelector('#CreateEventForm'));
        var template = '<div class="timerValue"><label>Timer Value: </label><input type="text"></div>';
        var compiled = $compile(template)($scope);
        console.log("compiled");
        formDiv.append(compiled);
        console.log("appending");
    };

    //used for associating a user with a new org
    $scope.associateUser = function(org){
        console.log("Associating a user with a new org now");
        console.log("Data received:");
        console.log(org);

        if(org == null){
            var alertEl = angular.element(document.querySelector('#orgAlert'));
            alertEl.removeClass('hide');
            alertEl.addClass('show');
        }
        else if('orgName' in org) {
            var orgName = org['orgName'];
            if (orgName.split(" ").length > 1 || orgName == " " || orgName == null) {
                var alertEl = angular.element(document.querySelector('#orgAlert'));
                alertEl.removeClass('hide');
            }
            else {
                $http.post('/API/associateUser', org).
                    success(function (data, status, headers, config) {
                        // this callback will be called asynchronously
                        // when the response is available
                        console.log("got response");
                        console.log(data);
                        if(data['error'] == null){
                            $scope.$parent.hasOrg = true;
                            window.localStorage.setItem("PIFhasOrg", true);

                            window.localStorage.setItem("PIForgID", data['org']['orgID']);

                            $scope.$parent.orgName = org['orgName'];
                            window.localStorage.setItem("PIForgName", org['orgName']);
                            angular.element(document.querySelector('#orgAlert')).addClass('hide');
                            $location.url('/profile');
                        }else{
                            var imaginaryAlert = angular.element(document.querySelector('#associateFail'));
                            imaginaryAlert.removeClass('hide');
                        }
                    }).
                    error(function (data, status, headers, config) {
                        // called asynchronously if an error occurs
                        // or server returns response with an error status.
                        console.log("ERROR: calling /API/orgs failed");
                    });
            }
        }
    };

    //used for creating a new org
    $scope.createOrg = function(org){
        console.log(org);
        if(org == null){
            var alertEl = angular.element(document.querySelector('#orgAlert'));
            alertEl.removeClass('hide');
            alertEl.addClass('show');
        }
        else if('orgName' in org) {
            var orgName = org['orgName'];
            if (orgName.split(" ").length > 1 || orgName == " " || orgName == null) {
                var alertEl = angular.element(document.querySelector('#orgAlert'));
                alertEl.removeClass('hide');
            }
            else {
                $http.post('/API/orgs', org).
                    success(function (data, status, headers, config) {
                        // this callback will be called asynchronously
                        // when the response is available
                        console.log("got valid orgname");
                        console.log(data);
                        $scope.$parent.hasOrg = true;
                        window.localStorage.setItem("PIFhasOrg", true);

                        window.localStorage.setItem("PIForgID", data['org']['orgID']);

                        $scope.$parent.orgName = org['orgName'];
                        window.localStorage.setItem("PIForgName", org['orgName']);
                        angular.element(document.querySelector('#orgAlert')).addClass('hide');
                        $location.url('/profile');
                    }).
                    error(function (data, status, headers, config) {
                        // called asynchronously if an error occurs
                        // or server returns response with an error status.
                        console.log("ERROR: calling /API/orgs failed");
                    });
            }
        }
    };


    //function logs in a user, probably should be named something other than "submit" for clarity
    $scope.login = function(user) {
        $http.post('/API/login', user).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                console.log(data);

                if(data['error'] != null){
                    var alertEl = angular.element(document.querySelector('#loginAlert'));
                    alertEl.removeClass('hide');
                }
                else{
                    console.log("Setting bullshit now");

//                    $scope.$parent.apikey = data['userPCM']['apiKey'];
//                    console.log("PCM: " + data['userPCM']);
//                    console.log("api key: " + String(data['userPCM']);
                    console.log("Setting API Key in local storage");
                    window.localStorage.setItem("PIFapiKey", data['userPCM']['apiKey']);


                    //storing logged in to storage
                    window.localStorage.setItem("PIFloggedIn", true);
                    $scope.loggedIn = true;

                    $scope.user = data['userPCM']['firstName'];
                    window.localStorage.setItem("PIFuserName", data['userPCM']['firstName']);
                    var orgID = data['userPCM']['orgID'];
                    //orgID == -1 implies user does not have a organization
                    //so if user has an org, set orgName variable in scope to be the associated org
                    if(orgID != -1){
                        $scope.$parent.hasOrg = true;
                        $scope.hasOrg = true;
                        window.localStorage.setItem("PIFhasOrg", true);

                        console.log("setting org ID in local storage");
                        window.localStorage.setItem("PIForgID", data['userPCM']['orgID']);

                        console.log("firing the get request");
                        $http.get('/API/orgs/'+orgID).
                          success(function(data, status, headers, config) {
                            var orgName = data['org']['orgName'];
                            console.log("org name should be " + orgName);
                            $scope.$parent.orgName = orgName;
                            $scope.orgName = orgName;
                            window.localStorage.setItem("PIForgName", data['org']['orgName']);
                          }).
                          error(function(data, status, headers, config) {
                          });
                    }
                    console.log("HIDING LOG IN ALERT NOW");
                    angular.element(document.querySelector('#loginAlert')).addClass('hide');
                    angular.element(document.querySelector('#signupAlert')).addClass('hide');
                    $location.url('/profile');
              }
            }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                console.log("ERROR: could not log in user");
              });
        };

    //function logs out a user
    $scope.logout = function() {
        $http.post('/API/logout').
            success(function(data, status, headers, config) {
                console.log(data);

                $scope.user = null;
//                $scope.loggedIn = false;
//                window.localStorage.setItem("PIFloggedIn", false);
                window.localStorage.clear();
                $scope.loggedIn = false;

                //may need to clear org
                $location.url('/logout');
            }).
            error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            console.log("ERROR: could not log out user");
            });
    };

    $scope.profile = function(){
        $location.url('/profile');
    };

    //register a new user, (no org association at first)
    $scope.registerSubmit = function(formData) {
        $http.post('/API/users', formData).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available

                if(data['error'] != null){
                    var alertEl = angular.element(document.querySelector('#signupAlert'));
                    alertEl.removeClass('hide');
                }
                else{
                    $scope.$parent.hasOrg = false;
                    window.localStorage.setItem("PIFhasOrg", false);



                    $scope.$parent.loggedIn = true;
                    window.localStorage.setItem("PIFloggedIn", true);

                    $scope.$parent.user = data['userPCM']['firstName'];
                    window.localStorage.setItem("PIFuserName", data['userPCM']['firstName']);

                    $scope.$parent.apikey = data['userPCM']['apikey'];
                    window.localStorage.setItem("PIFapiKey", data['userPCM']['firstName']);

                    angular.element(document.querySelector('#signupAlert')).addClass('hide');
                    angular.element(document.querySelector('#loginAlert')).addClass('hide');
                    $location.url('/profile');
                }
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                console.log("ERRORZZZZZ");
              });
        };
}]);
