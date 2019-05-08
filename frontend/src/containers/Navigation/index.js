import React, { Component } from 'react';
import { Segment,Header,Dropdown } from 'semantic-ui-react'
import './styles.scss';
import api from '../../api';

const yearList = [2016,2017,2018,2019]
const yearOptions = [
  {
    key:   2016,
    text: '2016',
    value: 2016,
  },
  {
    key:  2017,
    text:'2017',
    value:2017,
  },
  {
    key:   2018,
    text: '2018',
    value: 2018,
  },
  {
    key:  2019,
    text:'2016',
    value:2019,
  },
  {
    key:  'All',
    text:'2016-2019',
    value:'All',
  }

]
class Navigation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      hashtags: [],
    }
  }

  getHashtags = () => {
    api.getHashtags()
      .then(response => {
        this.setState({ hashtags: response.data });
      });
  };

  render() {
    const { hashtags } = this.state;

    return (
      <Segment raised className="Navigation">
        <Header size= "medium">Select Time Frame</Header>
        <div className="time-frame">
            <React.Fragment>
            {"Choose time  "}
             <Dropdown className="year"
               placeholder='Choose Year'
               // selection
               openOnFocus
               inline
               options={yearOptions}
             />{' '}
            </React.Fragment>
        </div>
        <div className="Navigation-buttons">

          <button
            type="button"
            onClick={this.getHashtags}
          >
            Top trending hashtags
          </button>
          <button
            type="button"
          >
            Top trending word
          </button>
          <button
            type="button"
          >
            Top trending word-pairs
          </button>
        </div>
        <div className="Navigation-options">
          {hashtags.map((hashtag, idx) => (
            <div id={idx}>
              {hashtag[0]}
            </div>
          ))}
        </div>
      </Segment>
    );
  }
}

export default Navigation;

