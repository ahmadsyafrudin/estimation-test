Feature: Client can estimate delivery
    For all delivery the estimates are as follows:
    Processing an order takes 1 day, so if customer estimates at Today,
    they should see that the fastest they receive it is in the next two days.
    Weekends don't count, so if they estimate on Friday, the fastest they can receive their shipment is on Tuesday.
    Holiday also doesn't count, so today is Monday and if tomorrow is a holiday,
    then the fastest they can receive their box is in the next 3 days.

  Scenario: client estimate for their order
    Given client want to order on 6 February 2019 at 13:00:00 GMT+7
    When estimate for delivery
    Then client get receive estimation on 8 February 2019 at 13:00:00 GMT+7

  Scenario: client estimate for their order and tomorrow is holiday
    Given client want to estimate order on 4 February 2019 at 13:00:00 GMT+7
    When estimate for delivery and tomorrow is holiday
    Then client get process estimation not tomorrow, but on 6 February 2019 at 13:00:00 GMT+7

  Scenario: client estimate for their order on holiday
    Given client want to estimate holiday order on 5 February 2019 at 13:00:00 GMT+7
    When estimate for delivery on holiday
    Then client can't do order because Chinese Lunar New Year's Day
