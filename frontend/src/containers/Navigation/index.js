import React, { Component } from 'react';
import { Segment, Header, Dropdown, Menu, Divider,Button } from 'semantic-ui-react'

import api from '../../api';
import './styles.scss';

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

  handleItemClick = (e, { name }) => {
    this.setState({ activeItem: name })
    if(name === 'hashtags'){
      this.getHashtags()
    }
    console.log(name)
  }

  getHashtags = () => {
    api.getHashtags()
      .then(response => {
        this.setState({ hashtags: response.data });
      });
  };

  render() {
    console.log("navigation", this.props.selection)
    const { hashtags } = this.state;
    const selection = this.props.selection
    const { activeItem } = this.state
    let spikeInfo = (
      <div>
        <React.Fragment>
        <Header className="mainHeader" size= "small">Select Time Frame</Header>            
             <Dropdown className="year"
               placeholder='Choose Year'
               // selection
               openOnFocus
               inline
               options={yearOptions}
             />
        </React.Fragment>
        <Header size= "small">Top 50 Trending</Header>
        <Menu className="contentMenu" widths={3} compact size='mini'>
          <Menu.Item name='unigrams' 
                     active={activeItem === 'unigrams'} 
                     onClick={this.handleItemClick} 
          />
          <Menu.Item name='hashtags' 
                     active={activeItem === 'hashtags'} 
                     onClick={this.handleItemClick} 
          />
          <Menu.Item name='wordpairs' 
                     active={activeItem === 'wordpairs'} 
                     onClick={this.handleItemClick} />
        </Menu>
        <Divider />
        <div className="Generated">
        <Header size= "small">Generated results: </Header>
        <div className="Navigation-options">
          {hashtags.map((hashtag, idx) => (
            <Button className="resultButton" id={idx} size='mini'   inverted color='grey'>
              {hashtag[0]}
            </Button>
          ))}
        </div>
        </div>
      </div>
      
    )

    let navigationInfo = spikeInfo
    if(selection === 'events'){
      navigationInfo = (
        <div>
          events
        </div>
      )
    }else if(selection === 'topics'){
      navigationInfo = (
        <div>
          topics
        </div>
      )
    }else{
      navigationInfo = spikeInfo
    }

    return (
      <Segment raised className="Navigation">
        {navigationInfo}
      </Segment>
    );
  }
}

export default Navigation;

