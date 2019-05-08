import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Grid } from 'semantic-ui-react'
import Header from '../Header/';
import Navigation from '../Navigation/';
import Canvas from '../Canvas/';
import Selection from '../Selection/';
import './styles.scss';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};

    // this.handleData = this.handleData.bind(this);
  }

  handleDate = (name) => {
    console.log(name)

    this.setState({
      selection:name
    })
  }

  render() {
    console.log("app props", this.props)
    const { activeItem } = this.state
    return (
      <div
        className="App"
      >
        <Header/>
        <Selection addStateToParent={this.handleData}/>
        <Grid>
          <Grid.Row columns={2}>
            <Grid.Column width={4}>
              <Navigation/>            
            </Grid.Column>
            <Grid.Column width={12}>
              <Canvas/>
            </Grid.Column>
          </Grid.Row>
        </Grid>

      </div>
    );
  }
}

export default App;

