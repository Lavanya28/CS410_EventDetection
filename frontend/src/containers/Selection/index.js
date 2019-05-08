import React, { Component } from 'react'
import { Menu } from 'semantic-ui-react'

class Selection extends Component {
	constructor(props) {
    super(props);

    this.state = {}
  }

  handleItemClick = (e, { name }) => {
  	this.setState({ activeItem: name })
  	console.log(this.props)
  	this.props.addStateToParent(this.state.activeItem);
  }
  

  render() {
  	const { activeItem } = this.state
    return (
        <Menu>
          <Menu.Item
            name='spikes'
            active={activeItem === 'spikes'}
            content='Spike Detection'
            onClick={this.handleItemClick}
          />

          <Menu.Item
            name='events'
            active={activeItem === 'events'}
            content='Event Detection'
            onClick={this.handleItemClick}
          />

          <Menu.Item
            name='topics'
            active={activeItem === 'topics'}
            content='Topic Modeling'
            onClick={this.handleItemClick}
          />
        </Menu>
    );
  }
}

export default Selection;