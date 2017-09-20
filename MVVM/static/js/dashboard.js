$(document).ready(function(){

    function Feature(data){
      var self = this
      self.title = ko.observable(data.title)
      self.description = ko.observable(data.description)
      self.client = ko.observable(data.client)
      self.priority = ko.observable(data.priority)
      self.due = ko.observable(data.due)
      self.productArea = ko.observable(data.productArea)
    }
   
    function FeatureViewModel(){
      var self = this
      self.clientList = ko.observableArray([])
      self.selectedClient = ko.observable()
      self.selectedSort = ko.observable('Priority')
      self.featureRequests = ko.observableArray([])
      self.currentFeatureIndex = ko.observable(0)
      self.totalRecords = ko.observable(0)
      self.displayNext = ko.computed(function() {
        return ((self.currentFeatureIndex() + 1) < self.totalRecords())
      })

      self.incrementIndex = function(){
          var previousCount = self.currentFeatureIndex()
          self.currentFeatureIndex(previousCount + 1)
      }

      self.decrementIndex = function(){
          var previousCount = self.currentFeatureIndex()
          self.currentFeatureIndex(previousCount - 1)
      }

      self.currentFeatureRequest = ko.computed(function(){
        return self.featureRequests()[self.currentFeatureIndex()]
      })
      
      self.addFeatureRequest = function(data){
        self.featureRequests.push(data)
      }
      
      self.loadFeatureRequests = function(){
        $.getJSON("/feature-request?sort=" + self.selectedSort(),function(data){
            self.featureRequests.removeAll()
            self.totalRecords(0)
            self.currentFeatureIndex(0)
            data.forEach(function(featureRequest){
              self.addFeatureRequest(featureRequest)
              self.totalRecords(self.totalRecords() + 1)
            })           
          })
      }

      ko.bindingHandlers.bsChecked = { //from stack overflow, ko and bs don't play nicely together
        init: function (element, valueAccessor, allBindingsAccessor,
        viewModel, bindingContext) {
            var value = valueAccessor();
            var newValueAccessor = function () {
                return {
                    change: function () {
                        value(element.value)
                    }
                }
            }
            ko.bindingHandlers.event.init(element, newValueAccessor,
            allBindingsAccessor, viewModel, bindingContext)
        },
        update: function (element, valueAccessor, allBindingsAccessor,
        viewModel, bindingContext) {
            if ($(element).val() == ko.unwrap(valueAccessor())) {
                 setTimeout(function () {
                    $(element).closest('.btn').button('toggle')
                 }, 1)
            }
        }
      }
    }

    $(function(){
      fvm = new FeatureViewModel()
      ko.applyBindings(fvm)
      fvm.loadFeatureRequests()
    });
})