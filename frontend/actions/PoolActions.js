import { CREATE_EVENT } from '../constants/ActionTypes';

export function createEvent(event) {
  return {
    type: CREATE_EVENT,
    event
  };
}
