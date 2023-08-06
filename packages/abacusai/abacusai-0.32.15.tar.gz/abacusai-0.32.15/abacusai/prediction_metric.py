from .return_class import AbstractApiClass


class PredictionMetric(AbstractApiClass):
    """
        A Prediction Metric job description.
    """

    def __init__(self, client, createdAt=None, featureGroupId=None, predictionMetricConfig=None, predictionMetricId=None, projectId=None):
        super().__init__(client, predictionMetricId)
        self.created_at = createdAt
        self.feature_group_id = featureGroupId
        self.prediction_metric_config = predictionMetricConfig
        self.prediction_metric_id = predictionMetricId
        self.project_id = projectId

    def __repr__(self):
        return f"PredictionMetric(created_at={repr(self.created_at)},\n  feature_group_id={repr(self.feature_group_id)},\n  prediction_metric_config={repr(self.prediction_metric_config)},\n  prediction_metric_id={repr(self.prediction_metric_id)},\n  project_id={repr(self.project_id)})"

    def to_dict(self):
        return {'created_at': self.created_at, 'feature_group_id': self.feature_group_id, 'prediction_metric_config': self.prediction_metric_config, 'prediction_metric_id': self.prediction_metric_id, 'project_id': self.project_id}
