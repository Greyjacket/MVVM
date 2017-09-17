$(document).ready(function(){

    function Feature(data){
      self.title = ko.observable(data.title)
      self.description = ko.observable(data.description)
      self.client = ko.observable(data.client)
      self.priority = ko.observable(data.priority)
      self.due = ko.observable(data.due)
      self.productArea = ko.observable(data.productArea)
      
      self.mapProperties = function(data){
        self.title(data.title)
        self.description(data.description)
        self.client(data.client)
        self.priority(data.priority)  
        self.due(data.due)
        self.productArea(data.productArea)  
      }
    }
    
    function FeatureViewModel(){
      var self = this;
      self.features = ko.observableArray([]);
      self.currentFeature = 0
      self.addFeature = function(data) {
        console.log(data)
        self.features.push(new Feature(data))
      }
    }

    fvm = new FeatureViewModel()
    ko.applyBindings(fvm)

    $.get("/feature-request", function(data, status){
      fvm.addFeature(data)
    })

})