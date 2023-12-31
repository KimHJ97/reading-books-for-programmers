# AWS IAM

AWS Identity and Access Management (IAM)은 Amazon Web Services (AWS)에서 제공하는 서비스 중 하나로, AWS 리소스에 대한 액세스를 안전하게 제어할 수 있게 해주는 웹 서비스입니다. IAM을 사용하면 AWS 계정 내에서 다양한 사용자, 그룹, 역할 등을 생성하고 관리하여 보안을 강화할 수 있습니다.  

 - 사용자(User)
    - AWS 계정에 액세스하는 개별적인 엔터티를 나타냅니다.
    - 각 사용자는 고유한 보안 자격 증명(Access Key ID 및 Secret Access Key)을 가지며, 이를 사용하여 AWS API 및 콘솔에 액세스할 수 있습니다.
 - 그룹(Group)
    - 여러 사용자에게 동일한 권한을 할당하기 위해 사용됩니다.
    - 그룹에 권한을 부여하면 해당 그룹의 모든 사용자가 해당 권한을 상속받습니다.
 - 권한 정책(Policy):
    - IAM 역할, 그룹 또는 사용자에게 할당되는 권한의 집합입니다.
    - JSON 형식으로 작성되며, 특정 작업 또는 리소스에 대한 권한을 정의합니다.
 - IAM 역할(Role)
    - AWS 리소스 간에 권한을 위임하기 위해 사용됩니다.
    - 역할은 일반적으로 AWS 서비스 간에 액세스를 허용하거나, 외부 엔터티에게 일시적으로 권한을 부여하는 데 사용됩니다.
 - 액세스 키(Access Key)
    - AWS API에 액세스하는 데 사용되는 보안 자격 증명으로, Access Key ID와 Secret Access Key로 구성됩니다.
 - MFA(Multi-Factor Authentication)
    - 사용자가 로그인할 때 추가적인 인증 수단을 사용하여 보안을 강화하는 기능입니다.
```
그룹
 - 사용자 하나씩 권한을 주는 것이 아니라, 그룹으로 권한을 부여한다.

권한 정책
 - 여러 개의 권한을 모아서 하나의 정책을 만든다.
 - 해당 정책을 각각의 그룹에 부여한다.

역할
 - 서비스에게 부여하는 권한의 모임
```

