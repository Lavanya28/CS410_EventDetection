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
    this.state = {
      selection: "",
      path: "",
      title: "",
      hashtags: [],
    }
  }

  addStateToParent = (name) => {
    this.setState({
      selection: name
    })
  }

  changePlot = (path, title) => {
    this.setState({ path, title });
  }

  changeHashtags = (hashtags) => {
    this.setState({ hashtags });
  }

  render() {
    const{
      selection,
      path,
      title,
      hashtags,
    } = this.state;

    return (
      <div
        className="App"
      >
        <Header/>
        <Selection addStateToParent={this.addStateToParent}/>
        <Grid>
          <Grid.Row columns={2}>
            <Grid.Column width={4}>
              <Navigation
                selection={selection}
                changePlot={this.changePlot}
                changeHashtags={this.changeHashtags}
              />
            </Grid.Column>
            <Grid.Column width={12}>
              <Canvas
                path={path}
                title={title}
                hashtags={hashtags}
                selection={selection}
              />
            </Grid.Column>
          </Grid.Row>
        </Grid>

      </div>
    );
  }
}

export default App;

