$(document).ready(function(){
    var initialData = [{title: "default", client: "default", description: "default", productArea: "default",
      priority: "default", "due": "default"} ]

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
      self.sortingOptions = ko.observableArray(['Most Recent', 'Priority'])
      self.selectedSort = ko.observable('Most Recent')
      self.featureRequests = ko.observableArray([])
      self.currentFeatureIndex = ko.observable(0)
      
      self.incrementIndex = function() {
          var previousCount = self.currentFeatureIndex()
          self.currentFeatureIndex(previousCount + 1)
      }

      self.decrementIndex = function() {
          var previousCount = self.currentFeatureIndex()
          self.currentFeatureIndex(previousCount - 1)
      }

      self.currentFeatureRequest = ko.computed(function() {
        return self.featureRequests()[self.currentFeatureIndex()]
      })
      
      self.addFeatureRequest = function(data) {
        self.featureRequests.push(data)
      }
      
      self.loadFeatureRequests = function(){
        $.getJSON("/feature-request", function(data){
            self.featureRequests.removeAll()
            self.addFeatureRequest(data)
          })
      }
    }

    $(function(){
      fvm = new FeatureViewModel()
      ko.applyBindings(fvm)
      fvm.loadFeatureRequests()
    });
})