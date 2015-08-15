import { CREATE_EVENT } from '../constants/ActionTypes';

let fixture = [
  {
    gameshow_slug: 'bb-17',
    title: 'Head of Household',
    date: new Date('2015-08-20T20:00:00'),
    date_performed: new Date('2015-08-20T20:00:00'),
    id: 10,
    choices: 1,
    matches_team: true,
  },
  {
    gameshow_slug: 'bb-17',
    title: 'Nominations',
    date: new Date('2015-08-23T20:00:00'),
    date_performed: new Date('2015-08-21T20:00:00'),
    id: 11,
    choices: 2,
    matches_team: false,
  },
  {
    gameshow_slug: 'bb-17',
    title: 'Power of Veto',
    date: new Date('2015-08-26T20:00:00'),
    date_performed: new Date('2015-08-24T20:00:00'),
    id: 12,
    choices: 1,
    matches_team: true,
  },
  {
    gameshow_slug: 'bb-17',
    title: 'Eviction',
    date: new Date('2015-08-27T20:00:00'),
    date_performed: new Date('2015-08-27T20:00:00'),
    id: 13,
    choices: 1,
    matches_team: false,
  },
];

export default function events(state=fixture, action) {
  switch (action.type) {
  case CREATE_EVENT:
    return [...state, action.event];
  default:
    return state;
  }
}
