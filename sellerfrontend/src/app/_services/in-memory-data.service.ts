import { InMemoryDbService } from 'angular-in-memory-web-api';
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const result = {
      'code': 0,
      'msg': "OK",
      'body': {
        'user_id': 1,
        'avatar': "img",
        'brand': "coca"
      }
    };
    return result;
  }
}