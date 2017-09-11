$(document).ready(function(){

        //handle a successful request
        function handleSuccess(){
          var successText = "Your feature request has been logged."
          $("#helper-display").html(successText).css({"display" : "block", "background-color":"#90d891"})
          $("#checkmark").css({"visibility" : "visible", "animation": "dash 2s ease-out forwards 1"})
          $("#checkmark-wrapper").css({"display" : "inline-block"})
        }

        //format the DOM according to the error received
        function handleErrors(error){
          switch(error){
            case '\'title\'':
              $("#title").css({"color": "red"})
              $("#title-input").css({"border-color": "red", "border-style": "solid"})
              var errorHelper = "Please provide a title for the feature request. All fields are required."
              break;
            case '\'description\'':
              $("#description").css({"color": "red"})
              $("#feature-description").css({"border-color": "red", "border-style": "solid"})
              var errorHelper = "Please provide a description for the feature request. All fields are required."
              break;
            case '\'selectedClient\'':
              $("#client").css({"color": "red"})
              $("#client-selector").css({"border-color": "red", "border-style": "solid"})
              var errorHelper = "Please select a client. All fields are required."
              break;
            case '\'date\'':
              $("#date").css({"color": "red"})
              $("#date-input").css({"border-color": "red", "border-style": "solid"})
              var errorHelper = "Please provide a due date for the feature request. All fields are required."
              break;
            case '\'productArea\'':
              $("#product_area").css({"color": "red"})
              var errorHelper = "Please select a product area for the feature request. All fields are required."
              break;
          }
          $("#helper-display").html(errorHelper).css({"display" : "block", "background-color":"#f2dede"})
        }

        //clear error formatting, if any
        function clear(){ 
          $("#title").css({"color": "black"})
          $("#title-input").css({"border-color": "#ccc"})
          $("#description").css({"color": "black"})
          $("#feature-description").css({"border-color": "#ccc"})
          $("#client").css({"color": "black"})
          $("#client-selector").css({"border-color": "#ccc"})
          $("#date").css({"color": "black"})
          $("#date-input").css({"border-color": "#ccc"})
          $("#product_area").css({"color": "black"})
          $("#helper-display").html("").css({"display" : "none"})
        }

        function featureModel() {
          var self = this;
          self.title = ko.observable();
          self.description = ko.observable();
          self.clients = ko.observableArray(['Client A', 'Client B', 'Client C'])
          self.selectedClient = ko.observable()
          self.priorityList = ko.observableArray(['1 (Urgent)', '2 (High)', '3 (Medium)', '4 (Low)'])
          self.selectedPriority = ko.observable('3 (Medium)')
          self.date = ko.observable()
          self.productArea = ko.observable()
          self.sendJSON = function() {
            clear()
            $.ajax({
              url: "/admin",
              type: "post",
              data: ko.toJSON(self),
              contentType: "application/json",
              success: function(data){
                handleSuccess()
              },
              error:function(jqXHR, textStatus, errorThrown) {
                handleErrors(jqXHR['responseJSON']['error'])
              }   
            }); 
          };
        }
          ko.bindingHandlers.bsChecked = { //from stack overflow, ko and bs don't play nicely together
            init: function (element, valueAccessor, allBindingsAccessor,
            viewModel, bindingContext) {
                var value = valueAccessor();
                var newValueAccessor = function () {
                    return {
                        change: function () {
                            value(element.value);
                        }
                    }
                };
                ko.bindingHandlers.event.init(element, newValueAccessor,
                allBindingsAccessor, viewModel, bindingContext);
            },
            update: function (element, valueAccessor, allBindingsAccessor,
            viewModel, bindingContext) {
                if ($(element).val() == ko.unwrap(valueAccessor())) {
                     setTimeout(function () {
                        $(element).closest('.btn').button('toggle');
                     }, 1); 
                }
            }
        }
        ko.applyBindings(new featureModel());
    });