Feature: Pickup estimation feature
    For all return orders, estimate the pickup time and the time they will be unbooked
    (unbooking means they can order the next shipment).
    Estimating on Monday means they will be picked up tomorrow, and processed and unbooked by Wednesday.
    Pickup can happen on Saturday, but not Sunday.
    Picking up on Saturday means being processed and unbooked on Monday.
    Holiday doesn't allow for processing, so estimating on today (Monday),
    and if the next 2 days is a holiday (Wednesday), then they will be unbooked on Thursday.

  Scenario: Client estimating their return
    Given client want to return on 11 February 2019 at 13:00:00 GMT+7
    When estimate for return
    Then client get pickup estimation on 12 February 2019 at 13:00:00 GMT+7

  Scenario: Client estimating their pickup on Saturday
    Given client estimate return on 8 February 2019 at 13:00:00 GMT+7
    When estimate for pickup on Saturday
    Then client get pickup and unbooked estimation on 11 February 2019 at 13:00:00 GMT+7

  Scenario: Holiday Doesnt allow for processing
    Given client estimate two days before Election day on 15 April 2019 at 13:00:00 GMT+7
    When estimate for pickup on Tuesday
    Then client get estimation for pickup and unbooked on 18 April 2019 at 13:00:00 GMT+7

  Scenario: Holiday Doesnt allow for return estimation
    Given client estimate on Election day on 17 April 2019 at 13:00:00 GMT+7
    When estimate for pickup and unbooked on Thursday
    Then client  cant get estimation for pickup and unbooked Because its Election Day