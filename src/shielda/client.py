from typing import Optional, Dict, Any, List
import requests


class ShieldaResponse:
    """Wrapper for Shielda verify API response."""

    def __init__(self, data: Dict[str, Any], raw_text: str = ""):
        self.data = data
        self.raw_text = raw_text
        self.success: bool = bool(data.get("success", False))
        self.challenge_ts: Optional[str] = data.get("challenge_ts")
        self.hostname: Optional[str] = data.get("hostname")
        self.error_codes: List[str] = data.get("error_codes", [])

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:
        return f"<ShieldaResponse success={self.success} errors={self.error_codes}>"


class Shielda:
    """Official client for verifying Shielda Captchas."""

    DEFAULT_VERIFY_URL = "https://shielda.ir/api/v1/siteverify"
    DEFAULT_WIDGET_URL = "https://shielda.ir/widget/api.js"
    DEFAULT_INPUT_NAME = "darban-captcha-response"

    def __init__(
        self,
        site_key: str,
        secret_key: str,
        verify_url: str = DEFAULT_VERIFY_URL,
        widget_url: str = DEFAULT_WIDGET_URL,
        timeout: float = 10.0,
    ):
        self.site_key = str(site_key)
        self.secret_key = str(secret_key)
        self.verify_url = verify_url
        self.widget_url = widget_url
        self.timeout = timeout
        self.last_result: Optional[ShieldaResponse] = None

    def verify(
        self,
        response: str,
        remote_ip: Optional[str] = None,
    ) -> bool:
        """Verify token and return boolean success status."""
        result = self.verify_with_details(response, remote_ip)
        return result.success

    def verify_with_details(
        self,
        response: str,
        remote_ip: Optional[str] = None,
    ) -> ShieldaResponse:
        """Verify token and return complete ShieldaResponse object."""
        if not response:
            res = ShieldaResponse({"success": False, "error_codes": ["missing-input-response"]})
            self.last_result = res
            return res

        if not self.secret_key:
            res = ShieldaResponse({"success": False, "error_codes": ["missing-secret-key"]})
            self.last_result = res
            return res

        payload = {
            "secret": self.secret_key,
            "response": response,
        }
        if remote_ip:
            payload["remoteip"] = remote_ip

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Shielda-Python/1.0.0",
        }

        try:
            r = requests.post(
                self.verify_url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            data = r.json()
            res = ShieldaResponse(data, raw_text=r.text)
            self.last_result = res
            return res
        except requests.RequestException as e:
            res = ShieldaResponse(
                {"success": False, "error_codes": ["http-connection-error"], "error_message": str(e)}
            )
            self.last_result = res
            return res
        except ValueError:
            res = ShieldaResponse(
                {"success": False, "error_codes": ["invalid-json-response"], "raw_body": r.text}
            )
            self.last_result = res
            return res

    def get_script_tag(self) -> str:
        """Returns the HTML script tag for Shielda widget."""
        return f'<script src="{self.widget_url}" async defer></script>'

    def get_widget_tag(self, theme: str = "auto", lang: str = "fa") -> str:
        """Returns the HTML widget container tag."""
        return (
            f'<div class="darban-captcha" data-sitekey="{self.site_key}" '
            f'data-theme="{theme}" data-lang="{lang}"></div>'
        )

    def render(self, theme: str = "auto", lang: str = "fa") -> str:
        """Returns both script and widget tag."""
        return f"{self.get_script_tag()}\n{self.get_widget_tag(theme, lang)}"
