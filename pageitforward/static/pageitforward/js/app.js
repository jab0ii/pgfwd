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
        
        .when('/signupAdmin', {templateUrl: '/static/pageitforward/landing/signupAdmin.html',
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

        // route for editing event handler
        .when('/editEventHandler',{
            templateUrl: '/static/pageitforward/eventHandlers/editEventHandler.html',
            controller: 'LandingCtlr'
        })

        // route for associating a user with org
        .when('/associateUser', {
            templateUrl: '/static/pageitforward/associateUser/associateUser.html',
            controller: 'LandingCtlr'
        })

        // route for editing contact method
        .when('/editContactMethod',{
            templateUrl: '/static/pageitforward/settings/editContactMethod.html',
            controller: 'LandingCtlr'
        })

        // route for the create org page
        .when('/eventHandlers', {
            templateUrl: '/static/pageitforward/eventHandlers/eventHandlers.html',
            controller: 'LandingCtlr'
        })

        // route for settings page
        .when('/settings', {
            templateUrl: '/static/pageitforward/settings/settings.html',
            controller: 'LandingCtlr'
        })

        .when('/createContactMethod', {
            templateUrl: 'static/pageitforward/settings/createContactMethod.html',
            controller: 'LandingCtlr'
        })

        .when('/viewEventHandlers', {
            templateUrl: 'static/pageitforward/eventHandlers/viewEventHandlers.html',
            controller: 'LandingCtlr'
        })

        // route for the create org page
        .when('/events', {
            templateUrl: '/static/pageitforward/events/events.html',
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

      $scope.checkModel = {
    left: false,
    right: false
  };
   $scope.bActive = false;
   $scope.changeClassLI = function(){
                console.log("shit called!!!!!!");

            $scope.currentPath = $location.path();
            console.log($scope.currentPath);
            if ($scope.currentPath === "/" || $scope.currentPath === "/logout"
                ||  $scope.currentPath === "/#" ) {
                    $scope.bActive = false;

            } else {
                    $scope.bActive = true;

            }
   }
    
    $scope.changeClassLI2 = function(){
                    $scope.bActive = true;

    }
    
    $scope.logoL = function(){
        $scope.bActive = false;
    }
    
    $scope.cUser = false;
    $scope.cAdmin = false;
    
    $scope.companyUser = function() {
        $scope.cAdmin = false;
        $scope.cUser = true;
    }
    
    $scope.companyAdmin = function() {
        $scope.cUser = false;
        $scope.cAdmin = true;
    }
    $scope.noInputError = true;

    $scope.subForm = function(formData, org) {
        if ($scope.cAdmin == true) {
            console.log('shitttSUMIITT');
            $scope.registerAdminSubmit(formData, org);
        } else {
            $scope.registerSubmit(formData, org);
        }
    }

//    $scope.$watch('defaultContactType', function(newValue, oldValue) {
//        console.log("defaultContactType changed");
//        console.log("old value:");
//        console.log(oldValue);
//        console.log("newValue");
//        console.log(newValue);
//    });




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
    };

    $scope.signupAdmin = function() {
        $location.url('/signupAdmin');
    }


    $scope.settings = function(){
        $location.url('/settings');
    };

    $scope.contactTypeOptions = [
    { name: 'Email', value: 'email' },
    { name: 'Phone', value: 'sms' }
    ];



    $scope.postContactMethod = function(){
        console.log("postContactMethod was called");
        var contactTypeEl = angular.element(document.querySelector('#contactType'));
        var contactDataEl = angular.element(document.querySelector('#contactData'));
        var successEl = angular.element(document.querySelector('#contactEditSuccess'));
        var failEl = angular.element(document.querySelector('#contactEditFail'));
        var titleEl = angular.element(document.querySelector('#title'));
        var priorityEl = angular.element(document.querySelector('#priority'));
        var editedCM = {};
//        console.log("priority");
        editedCM['priority'] = priorityEl.val();
//        console.log("title");
        editedCM['title'] = titleEl.val();
//        console.log("contactData");
        editedCM['contactData'] = contactDataEl.val();
//        console.log("contactType");
        editedCM['contactType'] = $scope.contactTypeOptions[contactTypeEl.val()].value;
//        console.log($scope.currentlyEditing);
        $http.post('/API/contactmethods/'+$scope.currentlyEditing, editedCM).
          success(function(data, status, headers, config) {
            if(data['success']){
                failEl.addClass('hide');
                successEl.removeClass('hide');
                listEl.addClass('wow');
                listEl.addClass('fadeOut');
                listEl.addClass('animated');
            }
            else{
                successEl.addClass('hide');
                failEl.removeClass('hide');
            }
          }).
          error(function(data, status, headers, config){
                console.log("Got error");
                successEl.addClass('hide');
                failEl.removeClass('hide');
          });

    };

    $scope.editContactMethod = function(contactMethod){

        console.log("Here is contactMethod we are editing");
        console.log(contactMethod);
//        var contactTypeEl = angular.element(document.querySelector('#contactType'));
//        var contactDataEl = angular.element(document.querySelector('#contactData'));
//        var titleEl = angular.element(document.querySelector('#title'));
//        var priorityEl = angular.element(document.querySelector('#priority'));
        $scope.$parent.editContactData = contactMethod['contactData'];
        $scope.$parent.editPriority = contactMethod['priority'];
        $scope.$parent.editTitle = contactMethod['title'];
        $scope.$parent.currentlyEditing = contactMethod['contactMethodID'];
//        console.log("contact method type is");
//        console.log(contactMethod['contactType']);
        $scope.$parent.defaultContactType = contactMethod['contactType'];
        $scope.defaultContactType = contactMethod['contactType'];
        $location.url('/editContactMethod');

    };
    $scope.deleteContactMethod = function(contactMethodID){
      var successEl = angular.element(document.querySelector('#contactDeleteSuccess'));
      var failEl = angular.element(document.querySelector('#contactDeleteFail'));
      var listEl = angular.element(document.querySelector('#contact'+contactMethodID));
      $http.delete('/API/contactmethods/'+contactMethodID).
          success(function(data, status, headers, config){
            if(data['success']){
                failEl.addClass('hide');
                successEl.removeClass('hide');
                listEl.addClass('wow');
                listEl.addClass('fadeOut');
                listEl.addClass('animated');
            }
            else{
                successEl.addClass('hide');
                failEl.removeClass('hide');
            }
          }).
          error(function(data, status, headers, config){
                console.log("Got error");
                successEl.addClass('hide');
                failEl.removeClass('hide');
          });
    };
     $scope.contactCreated= false;

    $scope.createContactMethod = function(newCM){
        console.log("Got new contact method request");
        console.log(newCM);
        var successEl = angular.element(document.querySelector('#contactCreateSuccess'));
        var failEl = angular.element(document.querySelector('#contactCreateFail'));

        $http.post('/API/contactmethods', newCM).
          success(function(data, status, headers, config) {
            console.log("GOT SUCCESS");
            console.log(data);
            if(data['success']){
                failEl.addClass('hide');
                successEl.removeClass('hide');
                $scope.contactCreated = true;
                console.log("CONTACTCREATED");
                console.log($scope.contactCreated);
        
            }
            else{
                successEl.addClass('hide');
                failEl.removeClass('hide');
            }
          }).
          error(function(data, status, headers, config) {
                console.log("Got error");
                successEl.addClass('hide');
                failEl.removeClass('hide');
          });
    };

    $scope.sendEvent = function(){
        var postData = {};
        var handlerSelection = angular.element(document.querySelector('#eventHandlerSelection'));
        var eventTitle = angular.element(document.querySelector('#eventTitle')).val();
        var eventMessage = angular.element(document.querySelector('#eventMessage')).val();
        var eventAPIKey = $scope.apiKey;
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
                    alert("Your page has been successfully sent!");
		    $scope.changeView("/profile");
                }	
                console.log(data);
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              });
    };

    $scope.createEvent = function(){
       if($scope.eventHandlers == null) {
           $http.get('/API/eventhandlers').
               success(function (data, status, headers, config) {
                   // this callback will be called asynchronously
                   // when the response is available
                   console.log("Got success from GET event handlers API");
                   console.log("RESPONSE:");
                   console.log(data);
//            console.log("This should be an array of event handlers");
//            console.log(data['eventHandlers']);
                   $scope.eventHandlers = data['eventHandlers'];
                   if ($scope.$parent != null) {
                       console.log("found null for eevnthandlers");
                       $scope.$parent.eventHandlers = data['eventHandlers'];
                   }

               }).
               error(function (data, status, headers, config) {
                   // called asynchronously if an error occurs
                   // or server returns response with an error status.
               });
       }
        $scope.changeView('/createEvent');
    };

    $scope.deleteEventHandler = function(handlerID){
      var successEl = angular.element(document.querySelector('#eventHandlerDeleteSuccess'));
      var failEl = angular.element(document.querySelector('#eventHandlerDeleteFail'));
      var listEl = angular.element(document.querySelector('#eventHandler'+handlerID));
        $http.delete('/API/eventhandlers/'+handlerID).
          success(function(data, status, headers, config) {
            if(data['success']){
                failEl.addClass('hide');
                successEl.removeClass('hide');
                listEl.addClass('wow');
                listEl.addClass('fadeOut');
                listEl.addClass('animated');
            }
            else{
                successEl.addClass('hide');
                failEl.removeClass('hide');
            }
          }).
          error(function(data, status, headers, config){
                console.log("Got error");
                successEl.addClass('hide');
                failEl.removeClass('hide');
          });
     };

    $scope.editEventHandler = function(eventHandler){
        $scope.changeView('/editEventHandler');
        console.log("Editing event handler");
        console.log(eventHandler);
        console.log("Title");
        console.log(eventHandler['title']);
        var hierarchy = angular.fromJson(eventHandler['hierarchy']);
        $scope.$parent.editEventHandlerTitle = eventHandler['title'];
        $scope.$parent.editEventHandlerID = eventHandler['eventHandlerID'];
    };





    $scope.addEditUser = function(user){
        console.log("Adding EDIT user");
        var currentHierarchyEl = angular.element(document.querySelector('#currentHierarchy'));
        console.log("currentHierarchyEl is ");
        console.log(currentHierarchyEl);
        var template = '<div class="userSelect"><label>Select User: </label><select><option ng-repeat="user in users" value="{{ user.id }}">{{ user.firstName }} {{ user.lastName }}</option></select></div>';
        var compiled = $compile(template)($scope);
        console.log("compiled");
        currentHierarchyEl.append(compiled);
        console.log("appending");
    };

    $scope.addEditLevel = function(timeout){
        console.log("Adding EDIT Event Handler Level");
        console.log("timeout value is " + timeout);
        var currentHierarchyEl = angular.element(document.querySelector('#currentHierarchy'));
        console.log("currentHierarchyEl is ");
        console.log(currentHierarchyEl);
        var template = '<div class="timerValue"><label>Timer Value: </label><p>' + String(timeout) + '</p></div>';
//        var compiled = $compile(template)($scope);
//        console.log("compiled");
        console.log("template is");
        console.log(template);
        console.log("appending");
        currentHierarchyEl.append(template);
    };





    $scope.viewEventHandlers = function(){
        if($scope.eventHandlers == null) {
            $http.get('/API/eventhandlers').
                success(function (data, status, headers, config) {
                    console.log("got event handlers");
                    console.log(data);
                    $scope.createdEventHandlers = data['eventHandlers'];
                    if ($scope.$parent != null) {
                        console.log("Found null for created Event handlrs");
                        $scope.$parent.createdEventHandlers = data['eventHandlers'];
                    }
                }).
                error(function (data, status, headers, config) {
                });
        }
        $scope.changeView('/viewEventHandlers');
    };



    $scope.postEditEventHandler = function(eventHandlerID){
        console.log("posting updated eventhandler");
        var postData = {};

        console.log("updated title is");
        var newTitleEl = angular.element(document.querySelector('#eventHandlerTitle'));
        postData['title'] = newTitleEl.val();
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
        console.log("FINAL POST DATA FOR UPDATED SHIT IS");
        console.log(postData);

        $http.post('/API/eventhandlers/'+eventHandlerID, postData).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                console.log("Got success from API endpoint");
                console.log("RESPONSE:");
                console.log(data);
                var successEl = angular.element(document.querySelector('#editEventHandlerCreateSuccess'));
                successEl.removeClass('hide');
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              });

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
            console.log(timerEl);
            console.log("TIME EL CHILD NODES BELOW, TIMER EL ELEMENT ABOVE");
            console.log(timerEl.childNodes);
            if(timerEl.childNodes.length == 7){

                var timerIn = timerEl.childNodes[3];
                console.log("Selected fourth element");
                console.log(timerIn);
            }
            else{
                var timerIn = timerEl.childNodes[2];
            }
            levelData["timeout"] = parseInt(timerIn.value);
            console.log("TIMER VALUE IS ");
            console.log(parseInt(timerIn.value));
            var siblingEl = timerEl.nextElementSibling;
            var users = [];
            while(siblingEl != null){

                if('className' in siblingEl && siblingEl.className == 'timerValue ng-scope'){
                    break;
                }

                if('className' in siblingEl &&
                    (siblingEl.className == 'userSelect'
                        || siblingEl.className == 'userSelect ng-scope')){
                    console.log("found user select");
                    var childNodes = siblingEl.childNodes;
                    console.log(childNodes.length);
                    console.log(childNodes);
                    if(childNodes.length == 7){
                        var selectEl = childNodes[3];
                        console.log(selectEl);
                        users.push(parseInt(selectEl.options[selectEl.selectedIndex].value));
                    }
                    if(childNodes.length==5){
                        var selectEl = childNodes[2];
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

    $scope.createEventHandler = function(){
        var orgID = $scope.orgID;
        console.log("createEventHandler was called");
        if(orgID == null){
            console.log("User trying to go to create event handler page without being associated");
        }
        else{
            $http.get('/API/orgUsers/'+orgID).
                success(function(data, status, headers, config){
                    console.log("Got response from API");
//                    console.log(data);
                    $scope.$parent.users = data['users'];
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

        var template = '<div class="userSelect"><label>Select User: </label> <select><option ng-repeat="user in users" value="{{ user.id }}">{{ user.firstName }} {{ user.lastName }}</option></select>       <button ng-click="removeHierarchyElement($event)"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></div>';
        var compiled = $compile(template)($scope);
        console.log("compiled");
        formDiv.append(compiled);
        console.log("appending");
    };

    $scope.addEventHandlerLevel = function(){
        console.log("Adding Event Handler Level");
        var formDiv = angular.element(document.querySelector('#CreateEventForm'));
        var template = '<div class="timerValue"><label>Timer Value: </label> <input class="timerinp" type="text">      <button ng-click="removeHierarchyElement($event)"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></div>';
        var compiled = $compile(template)($scope);
        console.log("compiled");
        formDiv.append(compiled);
        console.log("appending");
    };


    //remove event handler element
    $scope.removeHierarchyElement = function(obj){
        console.log("remove hierarchy element was called");
        console.log("First parent");
        console.log(obj.toElement.parentElement);
        var el = obj.toElement.parentElement;
        if(el.tagName != "DIV"){
            el = el.parentElement;
        }
        el.remove();
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
                            $scope.$parent.orgID = data['org']['orgID'];
                            $scope.$parent.orgName = org['orgName'];
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
                        $scope.$parent.orgID = data['org']['orgID'];
                        $scope.$parent.orgName = org['orgName'];
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
                console.log(data);

                if(data['error'] != null){
                    var alertEl = angular.element(document.querySelector('#loginAlert'));
                    if(alertEl.hasClass('hide')) {
                        alertEl.fadeIn().removeClass('hide');
                    } else {
                        alertEl.fadeOut(150).fadeIn(150);
                    }
                }
                else{
                    console.log("Setting bullshit now");
                    var userPCM = data['userPCM'];
                    $scope.apiKey = userPCM['apiKey'];
                    $scope.loggedIn = true;
                    $scope.bActive = true;
                    $scope.user = userPCM['firstName'];
                    $scope.contactMethods = userPCM['contactMethods'];
                    var orgID = userPCM['orgID'];
                    $scope.orgID = orgID;

                    //orgID == -1 implies user does not have a organization
                    //so if user has an org, set orgName variable in scope to be the associated org
                    if(orgID != -1){
                        $scope.hasOrg = true;
                        $http.get('/API/orgs/'+orgID).
                          success(function(data, status, headers, config) {
                            var orgName = data['org']['orgName'];
                            $scope.orgName = orgName;
                          }).
                          error(function(data, status, headers, config) {
                          });
                    }
                    console.log("HIDING LOG IN ALERT NOW");
                    angular.element(document.querySelector('#loginAlert')).addClass('hide');
                    angular.element(document.querySelector('#signupAlert')).addClass('hide');
                    var notCreate = angular.element(document.querySelector('#contactCreate'));

        if ($scope.contactCreated == true
) {
            
            notCreate.addClass('hide');
        }
                    $location.url('/profile');
              }
            }).
              error(function(data, status, headers, config) {
                console.log("ERROR: could not log in user");
              });
        };

    //function logs out a user
    $scope.logout = function() {
        $http.post('/API/logout').
            success(function(data, status, headers, config) {
                console.log(data);
                $scope.user = null;
                window.localStorage.clear();
                $scope.loggedIn = false;
                $scope.bActive = false;
                $location.url('/logout');
            }).
            error(function(data, status, headers, config) {
            console.log("ERROR: could not log out user");
            });
    };

    $scope.profile = function(){
        var notCreate = angular.element(document.querySelector('#contactCreate'));

        if ($scope.contactCreated == true
) {
            
            notCreate.addClass('hide');
        }
        $location.url('/profile');
    };

    //register a new user, (no org association at first)
    $scope.registerSubmit = function(formData, org) {
        $http.post('/API/users', formData).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available

		var options = {"show":false};


                if(data['error'] != null){
                    var alertEl = angular.element(document.querySelector('#signupAlert'));
		    console.log("Got an error, modal should not close");
                    alertEl.removeClass('hide');
                }
                else{
		    console.log("Hiding modal");
		    $('#myModal').modal('hide');
		    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                    $scope.$parent.hasOrg = false;
                    $scope.$parent.loggedIn = true;
                    $scope.$parent.bActive = true;
                    $scope.$parent.user = data['userPCM']['firstName'];
                    $scope.$parent.contactMethods = data['userPCM']['contactMethods'];
                    $scope.$parent.apikey = data['userPCM']['apikey'];
                    $scope.associateUser(org);
                    angular.element(document.querySelector('#signupAlert')).addClass('hide');
                    angular.element(document.querySelector('#loginAlert')).addClass('hide');
                    $scope.profile();
                }
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                console.log("ERRORZZZZZ");
              });
        };

    $scope.profile = function(){
		$location.url('/profile');	
	};

           //register a new user, (no org association at first)
    $scope.registerAdminSubmit = function(formData, org) {
        $http.post('/API/users', formData).
              success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                $scope.sAlert = false;
		var options = {"show":"false"};
                if(data['error'] != null){
                    var alertEl = angular.element(document.querySelector('#signupAlert'));
                    alertEl.removeClass('hide');
                    $scope.sAlert = true;
                }
                else{
		    console.log("hiding modal");
		    $('#myModal').modal('hide');
		    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                    $scope.$parent.hasOrg = false;
                    $scope.$parent.loggedIn = true;
                    $scope.$parent.bActive = true;
                    $scope.$parent.user = data['userPCM']['firstName'];
                    $scope.$parent.contactMethods = data['userPCM']['contactMethods'];
                    $scope.$parent.apikey = data['userPCM']['apikey'];
                    angular.element(document.querySelector('#signupAlert')).addClass('hide');
                    angular.element(document.querySelector('#loginAlert')).addClass('hide');
                    $scope.createOrg(org);
                    $scope.profile();
                }
              }).
              error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                console.log("ERRORZZZZZ");
              });

        };


    var init = function(){
            console.log("WE ARE INITIATING PAGE IT FORWARD!");
            $http.get('/API/loginStatus').
                success(function (data, status, headers, config) {
                    // this callback will be called asynchronously
                    // when the response is available
                    console.log("WE HAVE FOUND SUCCESS!: ");
                    var loggedIn = data['loggedIn'];
                    if (loggedIn && 'userPCM' in data) {
                        var userPCM = data['userPCM'];
                        console.log(userPCM);
                        $scope.loggedIn = true;
                        $scope.user = userPCM['firstName'];
                        $scope.apiKey = userPCM['apiKey'];
                        $scope.contactMethods = userPCM['contactMethods'];
                        var orgID = userPCM['orgID'];
                        $scope.orgID = orgID;
                        if (orgID != -1) {
                            $scope.hasOrg = true;
                            $http.get('/API/orgs/' + orgID).
                                success(function (data, status, headers, config) {
                                    $scope.orgName = data['org']['orgName'];
                                }).error(function (data, status, headers, config) {
                                });
                        }
                        else {
                            $scope.hasOrg = false;
                        }
                        console.log("Logged in and found userPCM in api response");

                    }
                    else {
                        $scope.loggedIn = false;
                        $scope.bActive = false;
                        console.log("User is not logged in");
                    }
                }).
                error(function (data, status, headers, config) {
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                    console.log(data);
                });
                $scope.changeClassLI();
                console.log("Checked login status");
                console.log("Now calling eventhandlers if user is logged in");

                if($scope.loggedIn) {
                    $http.get('/API/eventhandlers').
                        success(function (data, status, headers, config) {
                            console.log("got event handlers");
                            console.log(data);
                            $scope.eventHandlers = data['eventHandlers'];
                            console.log("set event handlers");
//                            if ($scope.$parent != null) {
//                                console.log("Found null for created Event handlrs");
//                                $scope.$parent.createdEventHandlers = data['eventHandlers'];
//                            }
                        }).
                        error(function (data, status, headers, config) {
                        });

                    console.log("if user has an org, also populating users var");
                    if($scope.hasOrg){
                        $http.get('/API/orgUsers/'+$scope.orgID).
                            success(function(data, status, headers, config){
                                console.log("Got response from ORG USERS API");
                                console.log(data);
                                $scope.users = data['users'];

                            }).
                            error(function(data, status, headers, config){
                               console.log("error calling api/orgusers");
                            });

                        $http.get('/API/getLogEvent').
                            success(function(data, status, headers, config){
                                console.log("GOT SUCCESS FROM LOG EVENT GET API");
                                if('logEvents' in data){
                                    console.log("HERE ARE LOG EVENTS");
                                    console.log(data['logEvents']);
                                    $scope.logEvents = data['logEvents'];
                                    for(var i = 0; i < $scope.logEvents.length; i++){
                                        var userID = $scope.logEvents[i].user;
                                        for(var user in $scope.users){
                                            if(user.id == userID){
                                                $scope.logEvents[i].user = user.firstName;
                                            }
                                        }
                                    }
                                }
                            }).
                            error(function(data, status, headers, config){
                               console.log("error calling api/getLogEvent");
                            });
                    }


                }

    };


    init();
    
   
}]);


