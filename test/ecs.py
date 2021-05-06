response = client.create_target_group(
    Name='string',
    Protocol='HTTP'|'HTTPS'|'TCP'|'TLS'|'UDP'|'TCP_UDP'|'GENEVE',
    ProtocolVersion='string',
    Port=123, # this is going to be dynamic as well according to the port
    VpcId='string',
    HealthCheckProtocol='HTTP'|'HTTPS'|'TCP'|'TLS'|'UDP'|'TCP_UDP'|'GENEVE',
    HealthCheckPort='string',
    HealthCheckEnabled=True|False,
    HealthCheckPath='string',
    HealthCheckIntervalSeconds=123,
    HealthCheckTimeoutSeconds=123,
    HealthyThresholdCount=123,
    UnhealthyThresholdCount=123,
    Matcher={
        'HttpCode': 'string',
        'GrpcCode': 'string'
    },
    TargetType='instance'|'ip'|'lambda',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ]
)

response = client.create_rule(
    ListenerArn='string',
    Conditions=[
        {
            'Field': 'string',
            'Values': [
                'string',
            ],
            'HostHeaderConfig': {
                'Values': [
                    'string',
                ]
            },
            'PathPatternConfig': {
                'Values': [
                    'string',
                ]
            },
            'HttpHeaderConfig': {
                'HttpHeaderName': 'string',
                'Values': [
                    'string',
                ]
            },
            'QueryStringConfig': {
                'Values': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ]
            },
            'HttpRequestMethodConfig': {
                'Values': [
                    'string',
                ]
            },
            'SourceIpConfig': {
                'Values': [
                    'string',
                ]
            }
        },
    ],
    Priority=123,
    Actions=[
        {
            'Type': 'forward'|'authenticate-oidc'|'authenticate-cognito'|'redirect'|'fixed-response',
            'TargetGroupArn': 'string',
            'AuthenticateOidcConfig': {
                'Issuer': 'string',
                'AuthorizationEndpoint': 'string',
                'TokenEndpoint': 'string',
                'UserInfoEndpoint': 'string',
                'ClientId': 'string',
                'ClientSecret': 'string',
                'SessionCookieName': 'string',
                'Scope': 'string',
                'SessionTimeout': 123,
                'AuthenticationRequestExtraParams': {
                    'string': 'string'
                },
                'OnUnauthenticatedRequest': 'deny'|'allow'|'authenticate',
                'UseExistingClientSecret': True|False
            },
            'AuthenticateCognitoConfig': {
                'UserPoolArn': 'string',
                'UserPoolClientId': 'string',
                'UserPoolDomain': 'string',
                'SessionCookieName': 'string',
                'Scope': 'string',
                'SessionTimeout': 123,
                'AuthenticationRequestExtraParams': {
                    'string': 'string'
                },
                'OnUnauthenticatedRequest': 'deny'|'allow'|'authenticate'
            },
            'Order': 123,
            'RedirectConfig': {
                'Protocol': 'string',
                'Port': 'string',
                'Host': 'string',
                'Path': 'string',
                'Query': 'string',
                'StatusCode': 'HTTP_301'|'HTTP_302'
            },
            'FixedResponseConfig': {
                'MessageBody': 'string',
                'StatusCode': 'string',
                'ContentType': 'string'
            },
            'ForwardConfig': {
                'TargetGroups': [
                    {
                        'TargetGroupArn': 'string',
                        'Weight': 123
                    },
                ],
                'TargetGroupStickinessConfig': {
                    'Enabled': True|False,
                    'DurationSeconds': 123
                }
            }
        },
    ],
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ]
)

response = client.register_task_definition(
    family='string',
    taskRoleArn='string',
    executionRoleArn='string',
    networkMode='bridge'|'host'|'awsvpc'|'none',
    containerDefinitions=[
        {
            'name': 'string',
            'image': 'string', # this is required from ECR
            'repositoryCredentials': {
                'credentialsParameter': 'string'
            },
            'cpu': 123,
            'memory': 123,
            'memoryReservation': 123,
            'links': [
                'string',
            ],
            'portMappings': [
                {
                    'containerPort': 123, # dynamic
                    'hostPort': 123, # this is supposed to be 3000 port?
                    'protocol': 'tcp'|'udp'
                },
            ],
            'essential': True|False,
            'entryPoint': [
                'string',
            ],
            'command': [
                'string',
            ],
            'environment': [ # this could be dynamic
                {
                    'name': 'string', # ONG_name
                    'value': 'string' # ong1
                },
            ],
            'environmentFiles': [
                {
                    'value': 'string',
                    'type': 's3'
                },
            ],
            'mountPoints': [
                {
                    'sourceVolume': 'string',
                    'containerPath': 'string',
                    'readOnly': True|False
                },
            ],
            'volumesFrom': [
                {
                    'sourceContainer': 'string',
                    'readOnly': True|False
                },
            ],
            'linuxParameters': {
                'capabilities': {
                    'add': [
                        'string',
                    ],
                    'drop': [
                        'string',
                    ]
                },
                'devices': [
                    {
                        'hostPath': 'string',
                        'containerPath': 'string',
                        'permissions': [
                            'read'|'write'|'mknod',
                        ]
                    },
                ],
                'initProcessEnabled': True|False,
                'sharedMemorySize': 123,
                'tmpfs': [
                    {
                        'containerPath': 'string',
                        'size': 123,
                        'mountOptions': [
                            'string',
                        ]
                    },
                ],
                'maxSwap': 123,
                'swappiness': 123
            },
            'secrets': [
                {
                    'name': 'string',
                    'valueFrom': 'string'
                },
            ],
            'dependsOn': [
                {
                    'containerName': 'string',
                    'condition': 'START'|'COMPLETE'|'SUCCESS'|'HEALTHY'
                },
            ],
            'startTimeout': 123,
            'stopTimeout': 123,
            'hostname': 'string',
            'user': 'string',
            'workingDirectory': 'string',
            'disableNetworking': True|False,
            'privileged': True|False,
            'readonlyRootFilesystem': True|False,
            'dnsServers': [
                'string',
            ],
            'dnsSearchDomains': [
                'string',
            ],
            'extraHosts': [
                {
                    'hostname': 'string',
                    'ipAddress': 'string'
                },
            ],
            'dockerSecurityOptions': [
                'string',
            ],
            'interactive': True|False,
            'pseudoTerminal': True|False,
            'dockerLabels': {
                'string': 'string'
            },
            'ulimits': [
                {
                    'name': 'core'|'cpu'|'data'|'fsize'|'locks'|'memlock'|'msgqueue'|'nice'|'nofile'|'nproc'|'rss'|'rtprio'|'rttime'|'sigpending'|'stack',
                    'softLimit': 123,
                    'hardLimit': 123
                },
            ],
            'logConfiguration': {
                'logDriver': 'json-file'|'syslog'|'journald'|'gelf'|'fluentd'|'awslogs'|'splunk'|'awsfirelens',
                'options': {
                    'string': 'string'
                },
                'secretOptions': [
                    {
                        'name': 'string',
                        'valueFrom': 'string'
                    },
                ]
            },
            'healthCheck': {
                'command': [
                    'string',
                ],
                'interval': 123,
                'timeout': 123,
                'retries': 123,
                'startPeriod': 123
            },
            'systemControls': [
                {
                    'namespace': 'string',
                    'value': 'string'
                },
            ],
            'resourceRequirements': [
                {
                    'value': 'string',
                    'type': 'GPU'|'InferenceAccelerator'
                },
            ],
            'firelensConfiguration': {
                'type': 'fluentd'|'fluentbit',
                'options': {
                    'string': 'string'
                }
            }
        },
    ],
    volumes=[
        {
            'name': 'string',
            'host': {
                'sourcePath': 'string'
            },
            'dockerVolumeConfiguration': {
                'scope': 'task'|'shared',
                'autoprovision': True|False,
                'driver': 'string',
                'driverOpts': {
                    'string': 'string'
                },
                'labels': {
                    'string': 'string'
                }
            },
            'efsVolumeConfiguration': {
                'fileSystemId': 'string',
                'rootDirectory': 'string',
                'transitEncryption': 'ENABLED'|'DISABLED',
                'transitEncryptionPort': 123,
                'authorizationConfig': {
                    'accessPointId': 'string',
                    'iam': 'ENABLED'|'DISABLED'
                }
            },
            'fsxWindowsFileServerVolumeConfiguration': {
                'fileSystemId': 'string',
                'rootDirectory': 'string',
                'authorizationConfig': {
                    'credentialsParameter': 'string',
                    'domain': 'string'
                }
            }
        },
    ],
    placementConstraints=[
        {
            'type': 'memberOf',
            'expression': 'string'
        },
    ],
    requiresCompatibilities=[
        'EC2'|'FARGATE',
    ],
    cpu='string',
    memory='string',
    tags=[
        {
            'key': 'string',
            'value': 'string'
        },
    ],
    pidMode='host'|'task',
    ipcMode='host'|'task'|'none',
    proxyConfiguration={
        'type': 'APPMESH',
        'containerName': 'string',
        'properties': [
            {
                'name': 'string',
                'value': 'string'
            },
        ]
    },
    inferenceAccelerators=[
        {
            'deviceName': 'string',
            'deviceType': 'string'
        },
    ]
)

response = client.create_service(
    cluster='string',
    serviceName='string',
    taskDefinition='string',
    loadBalancers=[
        {
            'targetGroupArn': 'string', # arn of target group
            'loadBalancerName': 'string',
            'containerName': 'string',
            'containerPort': 123
        },
    ],
    serviceRegistries=[ # not sure what this is
        {
            'registryArn': 'string',
            'port': 123,
            'containerName': 'string',
            'containerPort': 123
        },
    ],
    desiredCount=123,
    clientToken='string',
    launchType='EC2'|'FARGATE',
    capacityProviderStrategy=[
        {
            'capacityProvider': 'string',
            'weight': 123,
            'base': 123
        },
    ],
    platformVersion='string',
    role='string',
    deploymentConfiguration={
        'deploymentCircuitBreaker': {
            'enable': True|False,
            'rollback': True|False
        },
        'maximumPercent': 123,
        'minimumHealthyPercent': 123
    },
    placementConstraints=[
        {
            'type': 'distinctInstance'|'memberOf',
            'expression': 'string'
        },
    ],
    placementStrategy=[
        {
            'type': 'random'|'spread'|'binpack',
            'field': 'string'
        },
    ],
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                'string',
            ],
            'securityGroups': [
                'string',
            ],
            'assignPublicIp': 'ENABLED'|'DISABLED'
        }
    },
    healthCheckGracePeriodSeconds=123,
    schedulingStrategy='REPLICA'|'DAEMON',
    deploymentController={
        'type': 'ECS'|'CODE_DEPLOY'|'EXTERNAL'
    },
    tags=[
        {
            'key': 'string',
            'value': 'string'
        },
    ],
    enableECSManagedTags=True|False,
    propagateTags='TASK_DEFINITION'|'SERVICE',
    enableExecuteCommand=True|False
)

response = client.start_build(
    projectName='string',
    secondarySourcesOverride=[
        {
            'type': 'CODECOMMIT'|'CODEPIPELINE'|'GITHUB'|'S3'|'BITBUCKET'|'GITHUB_ENTERPRISE'|'NO_SOURCE',
            'location': 'string',
            'gitCloneDepth': 123,
            'gitSubmodulesConfig': {
                'fetchSubmodules': True|False
            },
            'buildspec': 'string',
            'auth': {
                'type': 'OAUTH',
                'resource': 'string'
            },
            'reportBuildStatus': True|False,
            'buildStatusConfig': {
                'context': 'string',
                'targetUrl': 'string'
            },
            'insecureSsl': True|False,
            'sourceIdentifier': 'string'
        },
    ],
    secondarySourcesVersionOverride=[
        {
            'sourceIdentifier': 'string',
            'sourceVersion': 'string'
        },
    ],
    sourceVersion='string',
    artifactsOverride={
        'type': 'CODEPIPELINE'|'S3'|'NO_ARTIFACTS',
        'location': 'string',
        'path': 'string',
        'namespaceType': 'NONE'|'BUILD_ID',
        'name': 'string',
        'packaging': 'NONE'|'ZIP',
        'overrideArtifactName': True|False,
        'encryptionDisabled': True|False,
        'artifactIdentifier': 'string',
        'bucketOwnerAccess': 'NONE'|'READ_ONLY'|'FULL'
    },
    secondaryArtifactsOverride=[
        {
            'type': 'CODEPIPELINE'|'S3'|'NO_ARTIFACTS',
            'location': 'string',
            'path': 'string',
            'namespaceType': 'NONE'|'BUILD_ID',
            'name': 'string',
            'packaging': 'NONE'|'ZIP',
            'overrideArtifactName': True|False,
            'encryptionDisabled': True|False,
            'artifactIdentifier': 'string',
            'bucketOwnerAccess': 'NONE'|'READ_ONLY'|'FULL'
        },
    ],
    environmentVariablesOverride=[
        {
            'name': 'string',
            'value': 'string',
            'type': 'PLAINTEXT'|'PARAMETER_STORE'|'SECRETS_MANAGER'
        },
    ],
    sourceTypeOverride='CODECOMMIT'|'CODEPIPELINE'|'GITHUB'|'S3'|'BITBUCKET'|'GITHUB_ENTERPRISE'|'NO_SOURCE',
    sourceLocationOverride='string',
    sourceAuthOverride={
        'type': 'OAUTH',
        'resource': 'string'
    },
    gitCloneDepthOverride=123,
    gitSubmodulesConfigOverride={
        'fetchSubmodules': True|False
    },
    buildspecOverride='string',
    insecureSslOverride=True|False,
    reportBuildStatusOverride=True|False,
    buildStatusConfigOverride={
        'context': 'string',
        'targetUrl': 'string'
    },
    environmentTypeOverride='WINDOWS_CONTAINER'|'LINUX_CONTAINER'|'LINUX_GPU_CONTAINER'|'ARM_CONTAINER'|'WINDOWS_SERVER_2019_CONTAINER',
    imageOverride='string',
    computeTypeOverride='BUILD_GENERAL1_SMALL'|'BUILD_GENERAL1_MEDIUM'|'BUILD_GENERAL1_LARGE'|'BUILD_GENERAL1_2XLARGE',
    certificateOverride='string',
    cacheOverride={
        'type': 'NO_CACHE'|'S3'|'LOCAL',
        'location': 'string',
        'modes': [
            'LOCAL_DOCKER_LAYER_CACHE'|'LOCAL_SOURCE_CACHE'|'LOCAL_CUSTOM_CACHE',
        ]
    },
    serviceRoleOverride='string',
    privilegedModeOverride=True|False,
    timeoutInMinutesOverride=123,
    queuedTimeoutInMinutesOverride=123,
    encryptionKeyOverride='string',
    idempotencyToken='string',
    logsConfigOverride={
        'cloudWatchLogs': {
            'status': 'ENABLED'|'DISABLED',
            'groupName': 'string',
            'streamName': 'string'
        },
        's3Logs': {
            'status': 'ENABLED'|'DISABLED',
            'location': 'string',
            'encryptionDisabled': True|False,
            'bucketOwnerAccess': 'NONE'|'READ_ONLY'|'FULL'
        }
    },
    registryCredentialOverride={
        'credential': 'string',
        'credentialProvider': 'SECRETS_MANAGER'
    },
    imagePullCredentialsTypeOverride='CODEBUILD'|'SERVICE_ROLE',
    debugSessionEnabled=True|False
)