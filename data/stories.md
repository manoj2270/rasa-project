## happy path
* greet
  - utter_greet

## show products form
* greet
  - utter_greet
* show_products
  - show_products_form
  - form{"name": "show_products_form"}
  - form{"name": null}
* affirm
  - utter_happy

## show products unhappy path
* greet
  - utter_greet
* show_products
  - show_products_form
  - form{"name": "show_products_form"}
* chitchat
  - utter_chitchat
  - show_products_form
  - form{"name": null}
* thankyou
  - utter_thankyou

## show products very  unhappy path
* greet
  - utter_greet
* show_products
  - show_products_form
  - form{"name": "show_products_form"}
* chitchat
  - utter_chitchat
  - show_products_form
* chitchat
  - utter_chitchat
  - show_products_form
* chitchat
  - utter_chitchat
  - show_products_form
  - form{"name": null}
* thankyou
  - utter_thankyou
## show products stop and continue
* greet
  - utter_greet
* show_products
  - show_products_form
  - form{"name": "show_products_form"}
* stop
  - utter_ask_continue
* affirm
  - show_products_form
  - form{"name": null}
* thankyou
  - utter_thankyou

## show products stop3
* show_products
  - show_products_form
  - form{"name": "show_products_form"}
* stop
  - utter_ask_continue
* affirm
  - show_products_form
  - form{"name": null}
* thankyou
  - utter_thankyou

## show products stop
* greet
  - utter_greet
* show_products
  - show_products_form
  - form{"name": "show_products_form"}
* stop
  - form{"name": null}
  - utter_ask_continue
* deny
  - utter_goodbye
  - form{"name": null}
  - slot{"requested_slot": null}

*thankyou
  - utter_thankyou

## show products stop 2
* show_products
  - show_products_form
  - form{"name": "show_products_form"}
* stop
  - form{"name": null}
  - utter_ask_continue
* deny
  - utter_goodbye
  - form{"name": null}
  - slot{"requested_slot": null}


## bot challenge
* bot_challenge
  - utter_iamabot

## show products
* greet
  - utter_greet
* show_products
  - show_products_form
  - form{"name": "show_products_form"}
  - form{"name": null}

## show products

* show_products
  - show_products_form
  - form{"name": "show_products_form"}
  - form{"name": null}
* affirm
  - utter_happy


## get history form
* greet
  - utter_greet
* get_history
  - show_history_form
  - form{"name": "show_history_form"}
  - form{"name": null}
* affirm
  - utter_happy

## get history unhappy path
* greet
  - utter_greet
* get_history
  - show_history_form
  - form{"name": "show_history_form"}
* chitchat
  - utter_chitchat
  - show_history_form
  - form{"name": null}
* thankyou
  - utter_thankyou

## get history very  unhappy path
* greet
  - utter_greet
* get_history
  - show_history_form
  - form{"name": "show_history_form"}
* chitchat
  - utter_chitchat
  - show_history_form
* chitchat
  - utter_chitchat
  - show_history_form
* chitchat
  - utter_chitchat
  - show_history_form
  - form{"name": null}
* thankyou
  - utter_thankyou
## get history stop and continue
* greet
  - utter_greet
* get_history
  - show_history_form
  - form{"name": "show_history_form"}
* stop
  - utter_ask_continue
* affirm
  - show_history_form
  - form{"name": null}
* thankyou
  - utter_thankyou

## get history stop3
* get_history
  - show_history_form
  - form{"name": "show_history_form"}
* stop
  - utter_ask_continue
* affirm
  - show_history_form
  - form{"name": null}
* thankyou
  - utter_thankyou

## get history stop
* greet
  - utter_greet
* get_history
  - show_history_form
  - form{"name": "show_history_form"}
* stop
  - form{"name": null}
  - utter_ask_continue
* deny
  - utter_goodbye
  - form{"name": null}
  - slot{"requested_slot": null}

*thankyou
  - utter_thankyou

## get history stop 2
* get_history
  - show_history_form
  - form{"name": "show_history_form"}
* stop
  - form{"name": null}
  - utter_ask_continue
* deny
  - utter_goodbye
  - form{"name": null}
  - slot{"requested_slot": null}

## show stats 1
*greet
  - utter_greet
*show_stats
  - action_show_stats
  - utter_did_that_help
* affirm
  - utter_happy
*thankyou
  - utter_thankyou

## show stats 2
*greet
  - utter_greet
*show_stats
  - action_show_stats
  - utter_did_that_help
*thankyou
  - utter_thankyou


## show stats 3
*show_stats
  - action_show_stats
  - utter_did_that_help
* affirm
  - utter_happy
*thankyou
  - utter_thankyou


## get price form
*get_price
  - action_get_price
  - utter_did_that_help
* affirm
  - utter_happy

## get price form
* greet
  - utter_greet
*get_price
  - action_get_price
  - utter_did_that_help
*deny
  - utter_goodbye
## get price form
* greet
  - utter_greet
*get_price
  - action_get_price
  - utter_did_that_help
* affirm
  - utter_happy

## task list
* greet
  - utter_greet
* task_list
  - action_task_list
* choose_list
  - action_dispatch_task

## task list
* task_list
  - action_task_list
* choose_list
  - action_dispatch_task

## task list
* greet
  - utter_greet
* task_list
  - action_task_list
* choose_list
  - action_dispatch_task
* deny
  - utter_goodbye

## task list
* greet
  - utter_greet
* task_list
  - action_task_list
* choose_list
  - action_dispatch_task
* affirm
  - utter_happy