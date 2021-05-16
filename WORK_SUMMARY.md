# Medicine PubSup Specifications

## Functional need
Trying to fight a pandemy, we must provide with **on demand** medicine tabs production.

1. _Patients_ publish _every second_ their own need of medicine tabs, between 1 and 30 tabs are needed each time
2. _Medicine makers_ are in charge of requested tabs realisation, each _tab cannot be made in less than 2 seconds_

Better than big sentences, the functional "big picture" description of the needed facility can be represented with following simplified chart, showing where functional decoupling would happen :     

![Functional big picture diagram](documentation/assets/functional.png)

## Distribution challenge
This whole system is by nature in need for _elastic_ resources, as :
- temporality involves decoupling and parallelisation
- pandemic evolution is unknown, and more patients are likely to need additional tabs

Following sequence diagram shows the actual challenge :     

![Functional sequence diagram](documentation/assets/functional_needed_parallel.png)

Indeed, patient requests an amount of tabs **every second**, whereas **each tab takes more than 2 seconds** to be made.    

More over, this is the lightest case, where there is only one patient who requests tabs. This _3 workers needed estimation_ is for 1 patient only...

In order to overcome this decoupling need, _Kubernetes Jobs_ can be launched on demand. These jobs allocations would be handled by cluster orchestrator.

## Auto scaling
As demonstrated, the whole facility has to lever some autoscaling features (provided by _Kubernetes_) and scale correctly without any human action.

However, regular _horizontal scaling_ would NOT do the job in our use case. Indeed, our _medicine makers_ (aka topic consumers) won't be using much CPU or memory, thus cannot be auto scaled by regular _Kubernetes autoscaler_ feature.

[Keda](https://keda.sh/) would be used, and allow autoscaling based on _Kafka_ messages delivery delay.

## Specifications

### Patient / producer
![Functional patient](documentation/assets/patient_functional.png)

### Medicine maker / consumer
![Functional medicine maker](documentation/assets/medicine_functional.png)
