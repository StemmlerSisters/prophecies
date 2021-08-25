import { Model } from '@vuex-orm/core'
import { defaultHeaders, responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import Choice from '@/models/Choice'
import TaskRecord from '@/models/TaskRecord'
import User from '@/models/User'

export default class TaskRecordReview extends Model {
  static entity = 'task-record-reviews'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      status: this.string(),
      note: this.string(null).nullable(),
      alternativeValue: this.string(null).nullable(),
      choiceId: this.attr(null),
      choice: this.belongsTo(Choice, 'choiceId'),
      taskRecordId: this.attr(null),
      taskRecord: this.belongsTo(TaskRecord, 'taskRecordId'),
      checkerId: this.attr(null),
      checker: this.belongsTo(User, 'checkerId'),
      history: this.hasMany(TaskRecordReview, 'taskRecordId'),
      selected: this.boolean(false)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-record-reviews/`,
    dataTransformer: responseNormalizer,
    actions: {
      find (id) {
        return this.get(`${id}/`)
      },
      save (id, { attributes = { }, relationships = { } } = { }) {
        const type = 'TaskRecordReview'
        const data = { type, id, attributes, relationships }
        return this.put(`${id}/`, { data }, { headers: defaultHeaders() })
      },
      selectChoice (id, { choice, ...attributes }) {
        return this.save(id, {
          attributes,
          relationships: {
            choice: {
              data: {
                type: 'Choice',
                id: choice.id
              }
            }
          }
        })
      }
    }
  }
}
