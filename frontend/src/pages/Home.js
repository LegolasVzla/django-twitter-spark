import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import * as FaIcons from "react-icons/fa";
import Jumbotron from 'react-bootstrap/Jumbotron'

function Home() {

    const customJumbotronStyle = {
        marginTop: '1rem',
        borderRadius: '1.5rem'
    };

    return (
        <Container>
            <Row>
                <Col xs={4} md={2}>

                </Col>
                <Col xs={10} md={8}>
                    <Jumbotron fluid style={customJumbotronStyle}>
                        <Container>
                            <h2>El Analizador de Tópicos de redes Sociales</h2>
                            <p style={{textAlign:'justify'}}>
                            <FaIcons.FaRegComment style={{marginRight: '0.5rem'}}/> Esta aplicación le permitirá realizar búsquedas sobre redes sociales, para saber si se está hablando bien o mal sobre una palabra buscada, mostrando estadísticas relacionadas a la misma a través del tiempo.
                            </p>
                        </Container>
                    </Jumbotron>

                </Col>
                <Col xs={4} md={2}>

                </Col>
            </Row>
        </Container>        
    )
}

export default Home