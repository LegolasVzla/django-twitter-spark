import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import Card from 'react-bootstrap/Card'
import CustomSentimentCard from '../components/CustomSentimentCard'
import CustomTwitterActionsCard from '../components/CustomTwitterActionsCard'
import CustomMessagesCard from '../components/CustomMessagesCard'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import * as FaIcons from "react-icons/fa";

  const sentimentCardItems = [
    {
        cardType: 'Success',
        icon: <FaIcons.FaRegSmile style={{fontSize: '2rem'}} />,
        score: '60%',
        sentiment: 'Positivo'
    },
    {
        cardType: 'Danger',
        icon: <FaIcons.FaRegFrown style={{fontSize: '2rem'}} />,
        score: '30%',
        sentiment: 'Negativo'
    },
    {
        cardType: 'Secondary',
        icon: <FaIcons.FaRegMeh style={{fontSize: '2rem'}} />,
        score: '10%',
        sentiment: 'Neutral'
    }
];

const twitterActionsCardItems = [
    {
        cardType: 'Danger',
        icon: <FaIcons.FaRegHeart style={{fontSize: '4rem', margin: '15px 5px 0px 5px'}} />,
        action: 'Me Gusta',
        value: '150'
    },
    {
        cardType: 'Info',
        icon: <FaIcons.FaRetweet style={{fontSize: '4rem', margin: '15px 5px 0px 5px'}} />,
        action: 'Retweet',
        value: '50'
    }
];

const topTweetsCardItems = [
    {
        "positiveTweetsTop": [
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1267497856778240001/npUcyqTx_normal.jpg",
                "account": "ActualidadRT",
                "tweet": "PayPal incorporará el bitcóin y otras criptomonedas en su sistema de pagos https://t.co/MJ2GgGSR98",
                "favorites": 137,
                "retweets": 61,
                "createdAt": "21 Oct 2020 13:42:00",
                "positiveSentimentScore": "0.4708942379409741",
                "negativeSentimentScore": "0.5291057620590262",
                "confidenceScore": "0.6"
            },
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1125178371422457858/o8VsuhX4_normal.jpg",
                "account": "aroliveros",
                "tweet": "Leo en el @FinancialTimes: PayPal pronto comenzará a ofrecer apoyo a las criptodivisas, ya que la compañía de pagos busca capitalizar el resurgimiento del interés de los consumidores, los comerciantes y los bancos centrales por monedas como el bitcoin y el etéreo.",
                "favorites": 114,
                "retweets": 47,
                "createdAt": "21 Oct 2020 16:01:46",
                "positiveSentimentScore": "0.8214818036205382",
                "negativeSentimentScore": "0.17851819637946045",
                "confidenceScore": "0.8"
            },
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1267638775569620992/LfLh9FNX_normal.jpg",
                "account": "whittoned",
                "tweet": "jaja como vas a invertir en bitcoin? que sos down?",
                "favorites": 0,
                "retweets": 0,
                "createdAt": "27 Oct 2020 18:08:04",
                "positiveSentimentScore": "0.3896065358617205",
                "negativeSentimentScore": "0.6103934641382793",
                "confidenceScore": "0.6"
            },
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1198211073993777152/xOfrCDNF_normal.jpg",
                "account": "muyhipocratico",
                "tweet": "Hay que armar una marcha de orgullo #bitcoin Es lo mínimo que podemos hacer para retribuir tanta alegría junta.",
                "favorites": 0,
                "retweets": 0,
                "createdAt": "27 Oct 2020 18:07:55",
                "positiveSentimentScore": "0.6794621629115785",
                "negativeSentimentScore": "0.32053783708842243",
                "confidenceScore": "0.6"
            },
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1163309369213247493/kG9-HtYZ_normal.jpg",
                "account": "alye",
                "tweet": "El interés por invertir en Bitcoin subió un 19% comparado con 2019, según el informe de Grayscale https://t.co/3wmqkcCp3r",
                "favorites": 0,
                "retweets": 0,
                "createdAt": "27 Oct 2020 18:07:22",
                "positiveSentimentScore": "0.32386847575234756",
                "negativeSentimentScore": "0.6761315242476517",
                "confidenceScore": "0.8"
            }
        ],
        "negativeTweetsTop": [
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1197066707879256064/S1wKbTpX_normal.jpg",
                "account": "xataka",
                "tweet": "Alguien ha enviado 88.857 bitcoins por un valor de casi mil millones de euros, la transacción Bitcoin de más valor de la historia https://t.co/xjO7sb84So https://t.co/6uXxjfehoJ",
                "favorites": 105,
                "retweets": 19,
                "createdAt": "27 Oct 2020 03:01:06",
                "positiveSentimentScore": "0.08258672221468423",
                "negativeSentimentScore": "0.917413277785317",
                "confidenceScore": "1.0"
            },
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1080283623155294209/tUG9Nc9E_normal.jpg",
                "account": "urunancy2002ya1",
                "tweet": "@Techconcatalina Yo descubrí que mi yerno también está interesado en Bitcoin, sabe del tema, me envia noticias y creo que debe estar acumulando 👍 el resto creen que hablo chino, me sorprende la juventud, no están enterados. Yo ya pasé de ser generación milenio hace rato y yo re entusiasmada !!🤷‍♀️",
                "favorites": 0,
                "retweets": 0,
                "createdAt": "27 Oct 2020 18:12:35",
                "positiveSentimentScore": "0.06671810198529406",
                "negativeSentimentScore": "0.9332818980147037",
                "confidenceScore": "1.0"
            },
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1171098505173229569/lDhAVJVW_normal.jpg",
                "account": "BitcoinFNewsES",
                "tweet": "Estas son las 2 razones por las que los traders dicen que el nivel de 13,875 dólares será la próxima resistencia “lógica” del precio de Bitcoin https://t.co/5QRO1AZuVL",
                "favorites": 0,
                "retweets": 0,
                "createdAt": "27 Oct 2020 18:12:00",
                "positiveSentimentScore": "0.30091754040238816",
                "negativeSentimentScore": "0.6990824595976113",
                "confidenceScore": "1.0"
            },
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/721696047/kuraga_normal.jpg",
                "account": "t_kuraga",
                "tweet": "@JuanJGarcia99 No. Lo pregunto para descartar que el bitcoin no sea dinero mercancía",
                "favorites": 0,
                "retweets": 0,
                "createdAt": "27 Oct 2020 18:11:26",
                "positiveSentimentScore": "0.05440487118076799",
                "negativeSentimentScore": "0.9455951288192319",
                "confidenceScore": "1.0"
            },
            {
                "profileImageUrl": "http://pbs.twimg.com/profile_images/1260279776327208967/XGPSS6vn_normal.jpg",
                "account": "BlockCapital1",
                "tweet": "Había negociado contratos perpetuos de XRP en Bitmex... Me fue bien he, si quieren aprender más en  BiCapital podrán observar más información y operaciones en el mercado spot de criptos y algunos derivados.\n#blockchain #bitcoin #criptomonedas #XRP #BitMEX https://t.co/zCzo2JbTKQ",
                "favorites": 0,
                "retweets": 0,
                "createdAt": "27 Oct 2020 18:11:25",
                "positiveSentimentScore": "0.33494897788726635",
                "negativeSentimentScore": "0.6650510221127344",
                "confidenceScore": "0.6"
            }
        ]
    }
];

function SearchTwitter() {
    return (
        <Container>
            <Row>
                <Col xs={4} md={2}>

                </Col>
                <Col xs={10} md={8}>
                    <Card style={{ marginTop: '1rem'}}>
                        <Card.Header>
                            <Breadcrumb>
                                <Breadcrumb.Item href="/">Home</Breadcrumb.Item>
                                <Breadcrumb.Item href="/search-twitter">Buscar en Twitter</Breadcrumb.Item>
                                <Breadcrumb.Item href="/search-twitter-result" active>Resultado de la Búsqueda</Breadcrumb.Item>
                            </Breadcrumb>
                        </Card.Header>
                        <Card.Body>
                            <Card.Title><h3>Resultado de su Búsqueda en Twitter</h3></Card.Title>
                            <Card.Text>
                                <FaIcons.FaRegComment/> Análisis de Sentimiento para la palabra:
                            </Card.Text>
                                <Row>
                                    <Col lg={true} style={{ marginTop: '1rem'}}>
                                        <CustomSentimentCard cardItems={sentimentCardItems[0]} />
                                        <CustomSentimentCard cardItems={sentimentCardItems[1]} />
                                        <CustomSentimentCard cardItems={sentimentCardItems[2]} />
                                    </Col>
                                    <Col lg={true} style={{ marginTop: '1rem'}}>
                                        <CustomTwitterActionsCard cardItems={twitterActionsCardItems[0]} />
                                        <CustomTwitterActionsCard cardItems={twitterActionsCardItems[1]} />
                                    </Col>
                                </Row>
                        </Card.Body>
                    </Card>
                    <CustomMessagesCard cardItems={topTweetsCardItems[0].positiveTweetsTop} cardTitle={'Top de Tweets Positivos'} />
                    <CustomMessagesCard cardItems={topTweetsCardItems[0].negativeTweetsTop} cardTitle={'Top de Tweets Negativos'}/>
                </Col>
                <Col xs={4} md={2}>

                </Col>
            </Row>
        </Container>        
    )
}

export default SearchTwitter