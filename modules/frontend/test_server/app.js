const express = require('express')
const spawn = require('threads').spawn;

const app = express()
app.use(express.json())
const port = 5423

var data = {
    tweets : [],
    stocks : []
}

function generateText(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  
    for (var i = 0; i < length; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));
  
    return text;
  }
  

spawn( async (input, done) => {
    const sleep = (waitTimeInMs) => new Promise(resolve => setTimeout(resolve, waitTimeInMs));
    while (true) {
        // sleep for 1 second
        await sleep(1000);
        // call done
        done({});
    }
})
.send({})
.on('message', (response)=> {
    // add random data to data
    data.tweets.push(generateTweet())
    data.stocks.push(generateStock())
})

app.post('/getData',(req,res)=>{
    res.send(data);
})

app.listen(port);
console.log('Server now listening on port '  + port);

function generateTweet() {
    var template = {
        "created_at": "Fri Jan 11 23:19:24 +0000 2019",
        "id": 1083865993468772400,
        "id_str": "1083865993468772353",
        "text": "Camiseta NEW PROJECT \n$ 79.900 \nAlmacén ATICO Cúcuta \nCll 11#3-77 centro \nWhatsapp 3008912591\n#newproject #camiseta… https://t.co/MGwIbT2W7w",
        "source": "<a href=\"http://instagram.com\" rel=\"nofollow\">Instagram</a>",
        "truncated": true,
        "in_reply_to_status_id": null,
        "in_reply_to_status_id_str": null,
        "in_reply_to_user_id": null,
        "in_reply_to_user_id_str": null,
        "in_reply_to_screen_name": null,
        "user": {
          "id": 311537084,
          "id_str": "311537084",
          "name": "ALMACEN ATICO",
          "screen_name": "ALMACENATICO",
          "location": "CALLE 11 #  3-77 CENTRO CUCUTA",
          "url": "http://WWW.FACEBOOK.COM/ATICO.ALMACEN",
          "description": null,
          "translator_type": "none",
          "protected": false,
          "verified": false,
          "followers_count": 319,
          "friends_count": 838,
          "listed_count": 3,
          "favourites_count": 32,
          "statuses_count": 8124,
          "created_at": "Sun Jun 05 16:35:13 +0000 2011",
          "utc_offset": null,
          "time_zone": null,
          "geo_enabled": true,
          "lang": "es",
          "contributors_enabled": false,
          "is_translator": false,
          "profile_background_color": "0099B9",
          "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
          "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
          "profile_background_tile": true,
          "profile_link_color": "ABB8C2",
          "profile_sidebar_border_color": "FFFFFF",
          "profile_sidebar_fill_color": "DDEEF6",
          "profile_text_color": "333333",
          "profile_use_background_image": true,
          "profile_image_url": "http://pbs.twimg.com/profile_images/959466446450581504/oGCC1R0G_normal.jpg",
          "profile_image_url_https": "https://pbs.twimg.com/profile_images/959466446450581504/oGCC1R0G_normal.jpg",
          "profile_banner_url": "https://pbs.twimg.com/profile_banners/311537084/1486570172",
          "default_profile": false,
          "default_profile_image": false,
          "following": null,
          "follow_request_sent": null,
          "notifications": null
        },
        "geo": {
          "type": "Point",
          "coordinates": [
            7.8860179,
            -72.5021372
          ]
        },
        "coordinates": {
          "type": "Point",
          "coordinates": [
            -72.5021372,
            7.8860179
          ]
        },
        "place": {
          "id": "00a0366f1f6cd7ff",
          "url": "https://api.twitter.com/1.1/geo/id/00a0366f1f6cd7ff.json",
          "place_type": "city",
          "name": "Cúcuta",
          "full_name": "Cúcuta, Colombia",
          "country_code": "CO",
          "country": "Colombia",
          "bounding_box": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  -72.606396,
                  7.721175
                ],
                [
                  -72.606396,
                  8.429989
                ],
                [
                  -72.34779,
                  8.429989
                ],
                [
                  -72.34779,
                  7.721175
                ]
              ]
            ]
          },
          "attributes": {}
        },
        "contributors": null,
        "is_quote_status": false,
        "extended_tweet": {
          "full_text": "Camiseta NEW PROJECT \n$ 79.900 \nAlmacén ATICO Cúcuta \nCll 11#3-77 centro \nWhatsapp 3008912591\n#newproject #camiseta #moda #hombre #ático #Cúcuta #cucutaeslomio #centro en Almacen ATICO https://t.co/Fo5hhr91fo",
          "display_text_range": [
            0,
            208
          ],
          "entities": {
            "hashtags": [
              {
                "text": "newproject",
                "indices": [
                  94,
                  105
                ]
              },
              {
                "text": "camiseta",
                "indices": [
                  106,
                  115
                ]
              },
              {
                "text": "moda",
                "indices": [
                  116,
                  121
                ]
              },
              {
                "text": "hombre",
                "indices": [
                  122,
                  129
                ]
              },
              {
                "text": "ático",
                "indices": [
                  130,
                  136
                ]
              },
              {
                "text": "Cúcuta",
                "indices": [
                  137,
                  144
                ]
              },
              {
                "text": "cucutaeslomio",
                "indices": [
                  145,
                  159
                ]
              },
              {
                "text": "centro",
                "indices": [
                  160,
                  167
                ]
              }
            ],
            "urls": [
              {
                "url": "https://t.co/Fo5hhr91fo",
                "expanded_url": "https://www.instagram.com/p/BsgzCkbB8qy/?utm_source=ig_twitter_share&igshid=1mmt9wzhp0aez",
                "display_url": "instagram.com/p/BsgzCkbB8qy/…",
                "indices": [
                  185,
                  208
                ]
              }
            ],
            "user_mentions": [],
            "symbols": []
          }
        },
        "quote_count": 0,
        "reply_count": 0,
        "retweet_count": 0,
        "favorite_count": 0,
        "entities": {
          "hashtags": [
            {
              "text": "newproject",
              "indices": [
                94,
                105
              ]
            },
            {
              "text": "camiseta",
              "indices": [
                106,
                115
              ]
            }
          ],
          "urls": [
            {
              "url": "https://t.co/MGwIbT2W7w",
              "expanded_url": "https://twitter.com/i/web/status/1083865993468772353",
              "display_url": "twitter.com/i/web/status/1…",
              "indices": [
                117,
                140
              ]
            }
          ],
          "user_mentions": [],
          "symbols": []
        },
        "favorited": false,
        "retweeted": false,
        "possibly_sensitive": false,
        "filter_level": "low",
        "lang": "es",
        "timestamp_ms": "1547248764756"
      }

      return template
}

function generateStock() {
    var template = {
        "symbol": "SNAP",
        "marketPercent": Math.random(),
        "bidSize": Math.random() * 400,
        "bidPrice": Math.random() * 400,
        "askSize": Math.random() * 400,
        "askPrice": Math.random() * 400,
        "volume": Math.floor(Math.random() * 300000),
        "lastSalePrice": Math.random() * 400,
        "lastSaleSize": Math.floor(Math.random() * 100),
        "lastSaleTime": new Date().getTime(),
        "lastUpdated": new Date().getTime(),
        "sector": "softwareservices",
        "securityType": "commonstock"
      }

    return template;
}