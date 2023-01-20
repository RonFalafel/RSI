
# RSI

RSI = Room Screen Immersion

Syncs a smart bulb to the average screen color to get a beter immersion experience.  
Great for **movies** and **gaming**.

## Supported Modes

1. Yeelight Mode - Connects directly to a Yeelight smart bulb.
2. Home Assistant Mode - Sends a webhook call to your Home Assistant that updates your light to your average screen color.

## Upcoming features

1. Dynamic screen sampling + light refresh rate that will be configurable from the GUI.
2. Yeelight bulb discovery that shows all bulbs in your LAN in the GUI.
3. Prettier GUI.
4. Bug fixes XD

### Home Assistant Webhooks

You will need to add 2 webhooks to your Home Assistant for using Home Assistant Mode:
1. Default white light webhook - used to return the lightbulb to a default white color.
 
 ```
 alias: White Light
  description: ''
  trigger:
    - platform: webhook
      webhook_id: white-light
  condition: []
  action:
    - service: yeelight.set_color_temp_scene # This is the service used for Yeelight Bulbs. I'm sure other bulbs have a similar service.
      data:
        brightness: 100 # You can adjust these values to control the default light scene.
        kelvin: 4000 # You can adjust these values to control the default light scene.
      target:
        device_id: <YOUR DEVICES HOME-ASSITANT ID>
  mode: single
```

2. HSV color updater - used to update the lightbulb to a new HSV (Hue Saturation Lightness) value sent from RSI.

```
  alias: HSV Webhook
  description: ''
  trigger:
    - platform: webhook
      webhook_id: hsv-webhook
  condition: # This whole part can be removed. It just makes sure that your light is on before trying to update the color.
    - condition: device
      type: is_on
      device_id: <YOUR DEVICES HOME-ASSITANT ID>
      entity_id: <YOUR ENTITIES HOME-ASSITANT ID>
      domain: light
  action:
    - service: yeelight.set_hsv_scene
      data:
        hs_color:
          - '{{ trigger.query.H }}'
          - '{{ trigger.query.S }}'
        brightness: '{{ trigger.query.V }}'
      target:
        device_id: <YOUR DEVICES HOME-ASSITANT ID>
  mode: single

```

### Contribute
Feel free to contribute to this repository!
